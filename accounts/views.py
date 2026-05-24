# ═══════════════════════════════════════════════════
# IMPORTS — সবার আগে
# ═══════════════════════════════════════════════════
import bcrypt
import random
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth.hashers import make_password, check_password
from django.db import connection

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Role, Address
from .authentication import UserAuthentication


# ═══════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════
def create_cart_for_user(user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT IGNORE INTO cart (user_id) VALUES (%s)",
            [user_id]
        )


def get_tokens(user):
    refresh = RefreshToken()
    refresh['user_id'] = user.user_id
    refresh['email'] = user.email
    refresh['role_id'] = user.role_id
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# ═══════════════════════════════════════════════════
# OTP / PASSWORD RESET
# ═══════════════════════════════════════════════════
@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    email = request.data.get('email', '').strip().lower()
    if not email:
        return Response({'error': 'ইমেইল দিন'}, status=400)

    if not User.objects.filter(email=email).exists():
        return Response({'error': 'এই ইমেইলে কোনো অ্যাকাউন্ট নেই'}, status=404)

    otp = str(random.randint(100000, 999999))
    cache.set(f'otp_{email}', make_password(otp), timeout=600)

    try:
        send_mail(
            subject='ঝুড়ি — পাসওয়ার্ড রিসেট OTP',
            message=f'আপনার OTP কোড: {otp}\n\nএই কোডটি ১০ মিনিটের জন্য বৈধ।\n\nযদি আপনি এটি অনুরোধ না করেন, অনুগ্রহ করে উপেক্ষা করুন।',
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({'error': f'ইমেইল পাঠাতে ব্যর্থ: {str(e)}'}, status=500)

    return Response({'message': 'OTP পাঠানো হয়েছে'})


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    email = request.data.get('email', '').strip().lower()
    otp   = request.data.get('otp', '').strip()

    if not email or not otp:
        return Response({'error': 'ইমেইল ও OTP দিন'}, status=400)

    hashed = cache.get(f'otp_{email}')
    if not hashed:
        return Response({'error': 'OTP মেয়াদ শেষ হয়ে গেছে। পুনরায় পাঠান।'}, status=400)

    if not check_password(otp, hashed):
        return Response({'error': 'OTP সঠিক নয়'}, status=400)

    cache.set(f'otp_verified_{email}', True, timeout=600)
    return Response({'message': 'OTP যাচাই সফল'})


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email        = request.data.get('email', '').strip().lower()
    new_password = request.data.get('new_password', '')

    if not email or not new_password:
        return Response({'error': 'সব তথ্য দিন'}, status=400)

    if len(new_password) < 6:
        return Response({'error': 'পাসওয়ার্ড কমপক্ষে ৬ অক্ষর হতে হবে'}, status=400)

    if not cache.get(f'otp_verified_{email}'):
        return Response({'error': 'OTP যাচাই করা হয়নি'}, status=400)

    user = User.objects.filter(email=email).order_by('-user_id').first()
    if not user:
        return Response({'error': 'ব্যবহারকারী পাওয়া যায়নি'}, status=404)

    new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password_hash = new_hash
    user.save()

    cache.delete(f'otp_{email}')
    cache.delete(f'otp_verified_{email}')
    return Response({'message': 'পাসওয়ার্ড পরিবর্তন সফল'})


@api_view(['POST'])
def change_password(request):
    try:
        jwt_auth = UserAuthentication()
        validated = jwt_auth.authenticate(request)
        if not validated:
            return Response({'error': 'লগইন করুন'}, status=401)
        user = validated[0]
    except Exception:
        return Response({'error': 'অবৈধ টোকেন'}, status=401)

    current_password = request.data.get('current_password', '')
    new_password     = request.data.get('new_password', '')

    if not current_password or not new_password:
        return Response({'error': 'সব ঘর পূরণ করুন'}, status=400)

    if len(new_password) < 6:
        return Response({'error': 'নতুন পাসওয়ার্ড কমপক্ষে ৬ অক্ষর হতে হবে'}, status=400)

    try:
        password_matches = bcrypt.checkpw(
            current_password.encode('utf-8'),
            user.password_hash.encode('utf-8')
        )
    except Exception:
        password_matches = False

    if not password_matches:
        return Response({'error': 'বর্তমান পাসওয়ার্ড সঠিক নয়'}, status=400)

    new_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user.password_hash = new_hash
    user.save()
    return Response({'message': 'পাসওয়ার্ড পরিবর্তন সফল'})


# ═══════════════════════════════════════════════════
# CLASS-BASED VIEWS
# ═══════════════════════════════════════════════════
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email    = request.data.get('email', '').strip().lower()
        password = request.data.get('password', '')

        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=400)

        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password.'}, status=401)

        try:
            password_matches = bcrypt.checkpw(
                password.encode('utf-8'),
                user.password_hash.encode('utf-8')
            )
        except Exception:
            password_matches = False

        if not password_matches:
            return Response({'error': 'Invalid email or password.'}, status=401)

        tokens = get_tokens(user)
        return Response({
            **tokens,
            'user': {
                'user_id':   user.user_id,
                'full_name': user.full_name,
                'email':     user.email,
                'phone':     user.phone,
                'role_id':   user.role_id,
            }
        })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        full_name = request.data.get('full_name', '').strip()
        email     = request.data.get('email', '').strip().lower()
        phone     = request.data.get('phone', '').strip()
        password  = request.data.get('password', '')

        if not full_name or not email or not password:
            return Response({'error': 'Full name, email, and password are required.'}, status=400)

        if len(password) < 6:
            return Response({'error': 'Password must be at least 6 characters.'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'An account with this email already exists.'}, status=400)

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        try:
            role = Role.objects.get(role_id=3)
        except Role.DoesNotExist:
            return Response({'error': 'System error: customer role not found.'}, status=500)

        user = User.objects.create(
            role=role,
            full_name=full_name,
            email=email,
            phone=phone or None,
            password_hash=password_hash,
            is_active=True,
        )

        return Response({
            'message': 'Account created successfully.',
            'user_id': user.user_id,
        }, status=201)


class ProfileView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes     = [IsAuthenticated]

    def get(self, request):
        user      = request.user
        addresses = Address.objects.filter(user=user)

        return Response({
            'user_id':   user.user_id,
            'full_name': user.full_name,
            'email':     user.email,
            'phone':     user.phone,
            'addresses': [
                {
                    'address_id':  a.address_id,
                    'label':       a.label,
                    'street':      a.street,
                    'city':        a.city,
                    'state':       a.state,
                    'postal_code': a.postal_code,
                    'country':     a.country,
                    'is_default':  a.is_default,
                }
                for a in addresses
            ]
        })


class AddAddressView(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes     = [IsAuthenticated]

    def post(self, request):
        user   = request.user
        street = request.data.get('street', '').strip()
        city   = request.data.get('city', '').strip()

        if not street or not city:
            return Response({'error': 'Street and city are required.'}, status=400)

        is_default = request.data.get('is_default', False)

        if is_default:
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        address = Address.objects.create(
            user=user,
            label=request.data.get('label', 'Home'),
            street=street,
            city=city,
            state=request.data.get('state', ''),
            postal_code=request.data.get('postal_code', ''),
            country=request.data.get('country', 'Bangladesh'),
            is_default=is_default,
        )

        return Response({
            'address_id': address.address_id,
            'message':    'Address saved successfully.'
        }, status=201)