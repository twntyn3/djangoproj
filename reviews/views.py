from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .forms import ReviewForm
from .models import Review
from .ml import predict_sentiment

# Тексты между фото (30 штук) — будут лежать в reviews/content.py
# Если файла пока нет, сайт всё равно запустится (тексты будут пустыми).
try:
    from .content import LYRIC_CHUNKS
except Exception:
    LYRIC_CHUNKS = []


class SignIn(LoginView):
    template_name = "reviews/login.html"


class SignOut(LogoutView):
    pass


class Index(LoginRequiredMixin, View):
    template_name = "reviews/index.html"

    def get(self, request):
        form = ReviewForm()
        reviews = Review.objects.select_related("user").all()
        return render(request, self.template_name, {"form": form, "reviews": reviews})

    def post(self, request):
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.sentiment = predict_sentiment(review.text)
            review.save()
            return redirect("index")

        reviews = Review.objects.select_related("user").all()
        return render(request, self.template_name, {"form": form, "reviews": reviews})


class EditReview(LoginRequiredMixin, View):
    template_name = "reviews/edit.html"

    def get(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("Forbidden")

        form = ReviewForm(instance=review)
        return render(request, self.template_name, {"form": form, "review": review})

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("Forbidden")

        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.sentiment = predict_sentiment(review.text)
            review.save()
            return redirect("index")

        return render(request, self.template_name, {"form": form, "review": review})


class DeleteReview(LoginRequiredMixin, View):
    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        if review.user != request.user and not request.user.is_staff:
            return HttpResponseForbidden("Forbidden")

        review.delete()
        return redirect("index")


def music_page(request):
    """
    Новая вкладка: 30 фото + текст между каждым фото.
    Ожидаем картинки: reviews/static/reviews/img/01.jpg ... 30.jpg
    Тексты: reviews/content.py -> LYRIC_CHUNKS (список из 30 строк)
    """
    sections = []
    total_photos = 30

    for i in range(1, total_photos + 1):
        img_name = f"{i:02d}.jpg"  # 01.jpg ... 30.jpg
        text = LYRIC_CHUNKS[i - 1] if (i - 1) < len(LYRIC_CHUNKS) else ""
        sections.append(
            {
                "img": f"reviews/img/{img_name}",
                "text": text,
                "num": i,
            }
        )

    return render(request, "reviews/music.html", {"sections": sections})
