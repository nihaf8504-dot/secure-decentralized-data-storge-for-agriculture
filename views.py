from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login

from .models import Block
from .services import get_chain_status


# 🔐 Signup
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "signup.html", {
                "error": "All fields are required"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(username=username, password=password)
        login(request, user)

        return redirect('dashboard')

    return render(request, "signup.html")


# 🌐 Landing Page
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    return render(request, "index.html")


# 📊 Dashboard (Protected)
@login_required
def dashboard(request):
    status = get_chain_status()

    return render(request, "dashboard.html", {
        "total_blocks": Block.objects.count(),
        "is_valid": status["is_valid"],
        "error": status["error"],
        "error_block": status["block"]
    })


# ➕ Add Block (Protected)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Block, AuditLog


@login_required
def add_block_view(request):
    if request.method == "POST":
        data = request.POST.get("data")

        if data:
            # ✅ Create block and store reference
            block = Block.objects.create(
                data=data,
                user=request.user
            )

            # 🔥 Create audit log
            AuditLog.objects.create(
                user=request.user,
                block=block,
                action='CREATE',
                message=f"Block {block.index} created by {request.user.username}"
            )

        return redirect('dashboard')

    return render(request, "add_block.html")


# 📦 View Chain (Public or Protected — your choice)
@login_required
def view_chain(request):
    status = get_chain_status()

    blocks = Block.objects.order_by('index')

    return render(request, "chain.html", {
        "blocks": blocks,
        "error_block": status["block"]
    })

def about(request):
    return render(request,"about.html")


from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import AuditLog


@staff_member_required
def audit_logs_view(request):
    logs = AuditLog.objects.order_by('-timestamp')

    return render(request, "audit_logs.html", {
        "logs": logs
    })
