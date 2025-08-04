from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserPreferencesSerializer, ChangeEmailSerializer
from .models import UserProfile
from django.utils import timezone

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_preferences(request):
    """Handle user preferences."""
    if request.method == 'GET':
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(profile)
        return Response({
            'success': True,
            'preferences': serializer.data.get('preferences', {})
        })
    
    elif request.method == 'POST':
        # Get or create user profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserPreferencesSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'preferences': serializer.data.get('preferences', {})
            })
        return Response({
            'success': False,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_email(request):
    """Change user email."""
    serializer = ChangeEmailSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = request.user
        user.email = serializer.validated_data['new_email']
        user.save(update_fields=['email'])
        return Response({
            'success': True,
            'message': 'Email changed successfully'
        })
    return Response({
        'success': False,
        'error': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_preferences(request):
    """Reset user preferences to default values."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    profile.reset_preferences()
    return Response({
        'success': True,
        'preferences': profile.preferences
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_preferences(request):
    """Export user preferences as JSON file."""
    from django.http import JsonResponse
    from django.utils import timezone
    
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    export_data = {
        'exported_at': timezone.now().isoformat(),
        'user_id': request.user.id,
        'username': request.user.username,
        'preferences': profile.preferences
    }
    
    response = JsonResponse(export_data)
    response['Content-Disposition'] = f'attachment; filename="user_preferences_{request.user.username}_{timezone.now().strftime("%Y%m%d_%H%M%S")}.json"'
    return response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def import_preferences(request):
    """Import user preferences from JSON file."""
    try:
        import json
        file = request.FILES.get('file')
        if not file:
            return Response({
                'success': False,
                'error': 'No file provided'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        content = file.read().decode('utf-8')
        data = json.loads(content)
        
        if 'preferences' not in data:
            return Response({
                'success': False,
                'error': 'Invalid preferences file format'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.update_preferences(data['preferences'])
        
        return Response({
            'success': True,
            'preferences': profile.preferences
        })
    except json.JSONDecodeError:
        return Response({
            'success': False,
            'error': 'Invalid JSON file'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Get user statistics."""
    user = request.user
    
    # Calculate days since joining
    days_since_joined = (timezone.now() - user.date_joined).days
    
    # Calculate days since last login
    days_since_last_login = None
    if user.last_login:
        days_since_last_login = (timezone.now() - user.last_login).days
    
    stats = {
        'days_since_joined': days_since_joined,
        'days_since_last_login': days_since_last_login,
        'total_logins': getattr(user, 'login_count', 0),  # You might want to add this field
        'account_age_days': days_since_joined,
    }
    
    return Response({
        'success': True,
        'stats': stats
    })
