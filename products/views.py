from django.db.models import Avg, Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Category, Product, Review


class CategoryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all().order_by('category_id')
        return Response([
            {
                'category_id': c.category_id,
                'category_name': c.category_name,
                'parent_id': c.parent_id,
                'description': c.description,
            }
            for c in categories
        ])


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Product.objects.select_related('category').annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews'),
        )

        # Filter by category
        category_id = request.query_params.get('category')
        if category_id:
            # Include subcategories
            try:
                parent = Category.objects.get(category_id=category_id)
                child_ids = list(
                    Category.objects.filter(parent_id=category_id).values_list('category_id', flat=True)
                )
                cat_ids = [int(category_id)] + child_ids
                qs = qs.filter(category_id__in=cat_ids)
            except Category.DoesNotExist:
                pass

        # Search
        search = request.query_params.get('search', '').strip()
        if search:
            qs = qs.filter(
                Q(product_name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__category_name__icontains=search)
            )

        # Pagination
        page_size = int(request.query_params.get('page_size', 20))
        page = int(request.query_params.get('page', 1))
        total = qs.count()
        start = (page - 1) * page_size
        products = qs[start: start + page_size]

        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'results': [
                {
                    'product_id': p.product_id,
                    'product_name': p.product_name,
                    'description': p.description,
                    'price': str(p.price),
                    'stock_qty': p.stock_qty,
                    'image_url': p.image_url,
                    'category_id': p.category_id,
                    'category_name': p.category.category_name if p.category else '',
                    'avg_rating': round(float(p.avg_rating), 2) if p.avg_rating else 0,
                    'review_count': p.review_count or 0,
                }
                for p in products
            ]
        })


class ProductDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id):
        try:
            p = Product.objects.select_related('category').annotate(
                avg_rating=Avg('reviews__rating'),
                review_count=Count('reviews'),
            ).get(product_id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=404)

        reviews = Review.objects.filter(product=p).order_by('-created_at')[:10]

        return Response({
            'product_id': p.product_id,
            'product_name': p.product_name,
            'description': p.description,
            'price': str(p.price),
            'stock_qty': p.stock_qty,
            'image_url': p.image_url,
            'category_name': p.category.category_name if p.category else '',
            'avg_rating': round(float(p.avg_rating), 2) if p.avg_rating else 0,
            'review_count': p.review_count or 0,
            'reviews': [
                {
                    'review_id': r.review_id,
                    'user_id': r.user_id,
                    'rating': r.rating,
                    'comment': r.comment,
                    'created_at': str(r.created_at),
                }
                for r in reviews
            ]
        })