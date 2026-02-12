"""Custom context processors for TrimTrove."""
from authentication.models import Profile


def user_profile(request):
    """Add user_profile to context - None if not authenticated or no profile."""
    if request.user.is_authenticated:
        try:
            return {'user_profile': Profile.objects.get(user=request.user)}
        except Profile.DoesNotExist:
            return {'user_profile': None}
    return {'user_profile': None}
