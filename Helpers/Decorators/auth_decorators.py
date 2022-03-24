from django.shortcuts import redirect


def verified_acc_only(view_func):
    def wrap(request, *args, **kwargs):
        if request.user.is_verified_email:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('activation-required')

    return wrap


def not_verified_acc_only(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_verified_email:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')

    return wrap


def logout_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')

    return wrap


def superuser_required(view_func):
    def wrap(request, *args, **kwargs):
        if not request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('index')
    return wrap
