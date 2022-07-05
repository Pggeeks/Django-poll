from django.contrib.auth import logout
from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import Poll_Form
from .models import Option_Model, Question_Model, Voter
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from .forms import Register, loginform


@login_required(login_url="/")
def User_validate_poll(request, Poll_Obj):
    """
    Check if user already voted a question
    if not return True
    """
    if Voter.objects.filter(poll=Poll_Obj.poll, user=request.user).exists():
        messages.error(request, "You have already Voted")
        return False
    else:
        return True


@login_required(login_url="/")
def Create_View(request):
    """
    Get data from the Form and populate the database
    Please Check models Save method for Max 5 functionality
    """
    if request.method == "POST":
        form = Poll_Form(request.POST)
        if form.is_valid():
            try:
                Poll = form.save(commit=False)
                Poll.user = request.user
                Poll.save()
                Option_Model.objects.create(
                    poll=Poll,
                    option1=form.cleaned_data["choice1"],
                    option2=form.cleaned_data["choice2"],
                    option3=form.cleaned_data["choice3"],
                    option4=form.cleaned_data["choice4"],
                ).save()
                messages.success(request, "Poll Created successfully")
            except Exception:
                messages.error(request, "Maximum number of polls created")
            return redirect("/home/")
    else:
        form = Poll_Form()
    context = {
        "form": form,
    }
    return render(request, "pollapp/create.html", context=context)


@login_required(login_url="/")
def Home_View(request):
    """
    Show poll at the home page and validate the answers
    """
    if request.method == "POST":
        poll_id = request.POST["poll_id"]
        Poll_Obj = Option_Model.objects.get(poll=poll_id)
        if User_validate_poll(request, Poll_Obj):
            option = request.POST["Answer"]
            if option == "option1":
                Poll_Obj.option_1_count += 1
            elif option == "option2":
                Poll_Obj.option_2_count += 1
            elif option == "option3":
                Poll_Obj.option_3_count += 1
            elif option == "option4":
                Poll_Obj.option_4_count += 1
            else:
                return HttpResponse(400, "Invalid form")
            Voter.objects.create(poll=Poll_Obj.poll, user=request.user).save()
            Poll_Obj.save()
            messages.success(request, "Vote successfully submited")
        context = {"polls": Option_Model.objects.all(), "Result": Poll_Obj}
        return render(request, "pollapp/home.html", context=context)
    context = {"polls": Option_Model.objects.all()}
    return render(request, "pollapp/home.html", context=context)


def Profile(request):
    user_fetch = Question_Model.objects.filter(user=request.user)
    print(user_fetch)
    context = {
        "User_Object": User.objects.get(username=request.user),
        "mypolls": Option_Model.objects.filter(poll__in=user_fetch),
    }
    return render(request, "pollapp/profile.html", context=context)


# def Results_View(Ob):

#
class SignupView(FormView):
    template_name = "pollapp/signup.html"
    form_class = Register
    success_url = "/home/"

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        form.save()
        username = form.cleaned_data["username"]
        raw_password = form.cleaned_data["password1"]
        user_login = authenticate(username=username, password=raw_password)
        auth_login(self.request, user_login)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "pollapp/login.html"
    form_class = loginform
    success_url = "/home/"

    def form_valid(self, form):
        auth_login(self.request, form.cleaned_data)
        self.request.session["user"] = form.cleaned_data.email
        next_page = self.request.GET.get("next")
        if next_page is not None:
            return redirect(next_page)
        return super().form_valid(form)


def signout(request):
    logout(request)
    return redirect("/")
