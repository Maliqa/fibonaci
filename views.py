from django.shortcuts import render

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
    return render(request, "prediksi.html", {
        "hasil": hasil,
        "error": error,
        "last_result": last_result,
    })
