from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserForm
from .models import Users

def homePage(request):
    return render(request, "home.html", {"account_count": Users.objects.count()})

def add_new(request):
    form = UserForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created successfully.")
        return redirect("success")
    return render(request, "add_new.html", {"form": form})

def success(request):
    return render(request, "success.html")

def balance(request):
    user = None
    if request.method == "POST":
        account_number = request.POST.get("account_number", "").strip()
        user = Users.objects.filter(account_number=account_number).first()
        if not user:
            messages.error(request, "Account number not found.")
    return render(request, "balance.html", {"user": user})

def _amount(value):
    amount = Decimal(value)
    if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
        raise InvalidOperation
    return amount

def deposit(request):
    if request.method == "POST":
        account = request.POST.get("account_number", "").strip()
        try:
            amount = _amount(request.POST.get("amount", "").strip())
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid amount (up to 2 decimal places).")
            return redirect("deposit")
        try:
            with transaction.atomic():
                user = Users.objects.select_for_update().get(account_number=account)
                user.amount += amount
                user.save(update_fields=["amount"])
                messages.success(request, f"₹{amount:.2f} deposited. New balance: ₹{user.amount:.2f}")
        except Users.DoesNotExist:
            messages.error(request, "Account number not found.")
        return redirect("deposit")
    return render(request, "deposit.html")

def withdraw(request):
    if request.method == "POST":
        account = request.POST.get("account_number", "").strip()
        try:
            amount = _amount(request.POST.get("amount", "").strip())
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid amount (up to 2 decimal places).")
            return redirect("withdraw")
        try:
            with transaction.atomic():
                user = Users.objects.select_for_update().get(account_number=account)
                if user.amount < amount:
                    messages.error(request, "Insufficient balance.")
                else:
                    user.amount -= amount
                    user.save(update_fields=["amount"])
                    messages.success(request, f"₹{amount:.2f} withdrawn. Remaining balance: ₹{user.amount:.2f}")
        except Users.DoesNotExist:
            messages.error(request, "Account number not found.")
        return redirect("withdraw")
    return render(request, "withdraw.html")

def transfer(request):
    if request.method == "POST":
        source = request.POST.get("from_account", "").strip()
        destination = request.POST.get("to_account", "").strip()
        try:
            amount = _amount(request.POST.get("amount", "").strip())
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid amount (up to 2 decimal places).")
            return redirect("transfer")
        if not source or not destination:
            messages.error(request, "Enter both account numbers.")
            return redirect("transfer")
        if source == destination:
            messages.error(request, "Source and destination must be different.")
            return redirect("transfer")
        try:
            with transaction.atomic():
                locked = list(Users.objects.select_for_update().filter(
                    account_number__in=[source, destination]).order_by("pk"))
                accounts = {u.account_number: u for u in locked}
                sender, receiver = accounts.get(source), accounts.get(destination)
                if not sender or not receiver:
                    messages.error(request, "Source or destination account not found.")
                elif sender.amount < amount:
                    messages.error(request, "Insufficient balance.")
                else:
                    sender.amount -= amount
                    receiver.amount += amount
                    sender.save(update_fields=["amount"])
                    receiver.save(update_fields=["amount"])
                    messages.success(request, f"₹{amount:.2f} transferred. Remaining balance: ₹{sender.amount:.2f}")
        except Exception:
            messages.error(request, "Transfer could not be completed. Please try again.")
        return redirect("transfer")
    return render(request, "transfer.html")

def viewall(request):
    users = Users.objects.all().order_by("id")
    return render(request, "viewall.html", {"users": users})

def close_account(request):
    if request.method == "POST":
        account = request.POST.get("account_number", "").strip()
        confirm = request.POST.get("confirm") == "yes"
        if not confirm:
            messages.error(request, "Please confirm account closure.")
        else:
            user = Users.objects.filter(account_number=account).first()
            if not user:
                messages.error(request, "Account number not found.")
            elif user.amount != 0:
                messages.error(request, "Please withdraw or transfer the remaining balance before closing.")
            else:
                user.delete()
                messages.success(request, "Account closed successfully.")
                return redirect("home")
    return render(request, "close_account.html")

def about_us(request):
    return render(request, "about_us.html")

def user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account details updated.")
        return redirect("viewall")
    return render(request, "user_update.html", {"form": form, "user": user})

def user_delete(request, pk):
    user = get_object_or_404(Users, pk=pk)
    if request.method == "POST":
        if user.amount != 0:
            messages.error(request, "Account has a balance. Transfer or withdraw it before deletion.")
            return redirect("viewall")
        user.delete()
        messages.success(request, "Account deleted.")
        return redirect("viewall")
    return render(request, "user_delete.html", {"user": user})
