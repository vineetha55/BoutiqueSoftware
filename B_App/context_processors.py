from .models import ThemeSettings, ShopSettings

def global_settings(request):
    shop_settings = ShopSettings.objects.first()
    theme_settings = None
    if request.user.is_authenticated:
        try:
            theme_settings = ThemeSettings.objects.get(user=request.user)
        except ThemeSettings.DoesNotExist:
            theme_settings = None

    return {
        'settings': shop_settings,
        'theme': theme_settings
    }
