import sys
from django.conf import settings
from django.http import HttpResponse
from django.urls import path
from django.core.management import execute_from_command_line
from django.views.decorators.csrf import csrf_exempt  # Import ini!

HTML_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Generator Prediksi Togel 2D (Fibonacci)</title>
</head>
<body>
    <nav>
        <a href="/">Home</a> |
        <a href="/prediksi/">Prediksi</a>
    </nav>
    <hr>
    {content}
</body>
</html>
"""

def home_view(request):
    return HttpResponse(HTML_FORM.format(content="""
        <h1>Selamat Datang di Aplikasi Prediksi 2D!</h1>
        <p>Gunakan menu di atas untuk navigasi.</p>
    """))

def fibonacci_2d(seed, jumlah):
    angka1 = int(seed[0])
    angka2 = int(seed[1])
    hasil = []
    while len(hasil) < jumlah:
        next_angka = (angka1 + angka2) % 100
        prediksi = str(next_angka).zfill(2)
        if prediksi not in hasil and prediksi != seed:
            hasil.append(prediksi)
        angka1, angka2 = angka2, next_angka
    return hasil

@csrf_exempt  # Dekorator HARUS di sini!
def prediksi_view(request):
    hasil = []
    error = ""
    last_result = ""
    if request.method == "POST":
        last_result = request.POST.get("last_result", "")
        if not last_result.isdigit() or len(last_result) != 2:
            error = "Input harus 2 digit angka (misal: 23)"
        else:
            hasil = fibonacci_2d(last_result, 39)

    form = f"""
    <h1>Generator Prediksi Togel 2D (39 Output - Fibonacci)</h1>
    <form method="post">
        <label>Angka 2D terakhir:</label>
        <input type="text" name="last_result" maxlength="2" value="{last_result}">
        <button type="submit">Buat Prediksi</button>
    </form>
    """
    if error:
        form += f'<p style="color: red;">{error}</p>'
    if hasil:
        form += "<h2>39 Prediksi Angka 2D (Metode Fibonacci):</h2><ul>"
        for i, num in enumerate(hasil, 1):
            form += f"<li>{i}. {num}</li>"
        form += "</ul>"
    return HttpResponse(HTML_FORM.format(content=form))

settings.configure(
    DEBUG=True,
    SECRET_KEY='a',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=["*"],
    MIDDLEWARE=[
        "django.middleware.csrf.CsrfViewMiddleware",
    ],
)

urlpatterns = [
    path("", home_view, name="home"),
    path("prediksi/", prediksi_view, name="prediksi"),
]

if __name__ == "__main__":
    execute_from_command_line(sys.argv)
