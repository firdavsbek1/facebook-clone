import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from posts.models import Post
from .utils import justify_input_type, validate_fields, validate_username, check_new_password, validate_full_name, \
    get_friend_request_or_false, RequestFriendStatus
from .models import CustomUser, FriendList, FriendRequest
from datetime import date
from .forms import UserForm, UploadImageForm


def login_view(request):
    if request.POST.get('user_input') and request.POST.get('password'):
        user_input = request.POST['user_input']
        input_type = justify_input_type(user_input)
        if input_type:
            if input_type == 'email':
                user = CustomUser.objects.filter(email__iexact=user_input).first()
            elif input_type == 'phone':
                user = CustomUser.objects.filter(phone_number=user_input).first()
            else:
                user = CustomUser.objects.filter(username__iexact=user_input).first()
            if user:
                user_authenticated = authenticate(username=user.username, password=request.POST.get('password'))
                if user_authenticated:
                    login(request, user_authenticated)
                    messages.success(request, "You have successfully logged in.")
                    return redirect('accounts:profile',pk=user.pk)
    return render(request, 'registration/login.html')


def logout_view(reqeust):
    logout(reqeust)
    return redirect('accounts:login')


def register_view(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        user_input = data.get('user_input')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')
        day = data.get('date-birth')
        month = data.get('date-month')
        year = data.get('date-year')
        gender = data.get('gender-select')

        is_valid = validate_fields(first_name, last_name, user_input, password, day, month, year, gender)
        input_type = justify_input_type(user_input)
        print(input_type, is_valid)
        if is_valid and input_type:
            print("we are in here")
            if input_type == 'email':
                CustomUser.objects.create_user(
                    username=first_name.lower() + 'default',
                    email=user_input,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date(year=int(year), month=int(month), day=int(day)),
                    gender=gender
                )
                return redirect('accounts:login')
                # send welcome email
            elif input_type == 'phone':
                CustomUser.objects.create_user(
                    username=first_name.lower() + 'default',
                    phone_number=user_input,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date(year=year, month=month, day=day),
                    gender=gender
                )
                return redirect('accounts:login')
                # send welcome message
    return render(request, 'registration/register.html')


@login_required
def profile_page(request,pk):
    profile_being_seen=CustomUser.objects.get(id=pk)
    context={
        'user':profile_being_seen,
        'posts':profile_being_seen.posts.all()
    }
    is_friend=False
    try:
        friends=FriendList.objects.get(user=profile_being_seen).friends.all()
    except FriendList.DoesNotExist:
        friends=FriendList.objects.create(user=profile_being_seen).friends.all()
    if request.user in friends:
        is_friend=True
    if request.user != profile_being_seen and is_friend is False:
        friend_reqeust_to_me=get_friend_request_or_false(sender=profile_being_seen, receiver=request.user)
        if friend_reqeust_to_me is not False:
            request_sent=RequestFriendStatus.THEM_SENT_YOU.value
            context['friend_request_to_me']=friend_reqeust_to_me.id
        elif get_friend_request_or_false(sender=request.user,receiver=profile_being_seen) is not False:
            request_sent=RequestFriendStatus.YOU_SENT_THEM.value
        else:
            request_sent=RequestFriendStatus.NO_REQUEST_SENT.value
        context['request_sent']=request_sent
    else:
        friend_requests=FriendRequest.objects.filter(receiver=request.user,is_active=True)
        context['friend_requests']=friend_requests
    context['is_friend']=is_friend
    context['friends']=friends
    if request.method == 'POST':
        user = request.user
        form=UploadImageForm(instance=user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile',pk=user.id)

    return render(request, "accounts/profile.html",context)


@login_required
def profile_edit(request):
    logged_in_user = request.user
    if request.method == 'POST':
        data= {}
        data['password']=logged_in_user.password
        data['username']=request.POST.get('username')
        data['email']=request.POST.get('email')
        data['phone_number']=request.POST.get('phone_number')
        data['from_location']=request.POST.get('from_location')
        data['lives']=request.POST.get('lives')
        data['studied']=request.POST.get('studied')
        data['works_at']=request.POST.get('works_at')
        data['bio']=request.POST.get('bio')
        form = UserForm(instance=logged_in_user, data=data, files=request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # username validation
            if not user.validate_username(request.POST.get('username')) or not validate_username(
                    request.POST.get('username')):
                form.add_error('username', "Already exists or can't be validated. Please choose another one!")
            # password validation
            user.save()
            if request.POST.get('current_password'):
                if not user.validate_password(request.POST.get('current_password')):
                    form.add_error('password', "Not match with the user password!")
            response = check_new_password(request.POST.get('password1'), request.POST.get('password2'))
            if not response.get('success'):
                form.add_error('password', response.get('message'))
            # parsing full name to first_name and last_name
            user.first_name, user.last_name = validate_full_name(request.POST.get('name'))
            # creating date object of user with taking different inputs(day,month,year)
            user.date_of_birth = date(day=int(request.POST.get('date-birth')),
                                      month=int(request.POST.get('date-month')),
                                      year=int(request.POST.get('date-year'))
                                      )
            if not form.errors:
                if request.POST.get('password1',None):
                    user.set_password(request.POST.get('password1'))
                user.save()
                return redirect('accounts:profile',pk=user.pk)

        return render(request, 'accounts/profile-edit.html', {'user': logged_in_user, 'form': form})
    return render(request, 'accounts/profile-edit.html', {'user': logged_in_user})


@login_required
def trigger_request(request,friend_id):
    me_account=get_object_or_404(CustomUser,id=request.user.id)
    friend=get_object_or_404(CustomUser,id=friend_id)
    FriendRequest.objects.create(sender=me_account,receiver=friend)
    return redirect('accounts:profile',pk=friend_id)


def trigger_accept(request,request_id):
    friend_request=get_object_or_404(FriendRequest,id=request_id)
    friend_request.accept()
    return redirect('accounts:profile',pk=friend_request.sender.id)


def trigger_unfriend(request,friend_id):
    me_account=get_object_or_404(CustomUser,id=request.user.id)
    friend=get_object_or_404(CustomUser,id=friend_id)
    me_account.friend_list.unfriend(friend)
    return redirect('accounts:profile', pk=friend_id)


def trigger_cancel(request,friend_id):
    friend_request=FriendRequest.objects.get(sender_id=request.user.id,receiver_id=friend_id,is_active=True)
    friend_request.cancel()
    return redirect('accounts:profile', pk=friend_id)


def trigger_decline(request,request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    friend_request.decline()
    return redirect('accounts:profile', pk=friend_request.sender.id)

