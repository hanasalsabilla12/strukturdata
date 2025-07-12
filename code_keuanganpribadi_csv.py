import csv
import os
import datetime

FILE_NAME = "transaksi.csv"

# Header CSV
FIELDNAMES = ["tahun", "tanggal", "kategori", "nominal", "pemasukan", "pengeluaran"]

def load_data():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def save_data(data):
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data)

def tambah_transaksi(data):
    tanggal_str = input("Masukkan tanggal (dd-mm-yyyy): ")
    kategori = input("Masukkan kategori (misal: Makan, Transportasi): ")
    nominal = int(input("Masukkan jumlah nominal (angka saja): "))
    jenis = input("Jenis transaksi (pemasukan/pengeluaran): ").lower()

    tahun = tanggal_str.split('-')[2]
    pemasukan = nominal if jenis == "pemasukan" else 0
    pengeluaran = nominal if jenis == "pengeluaran" else 0

    data.append({
        "tahun": tahun,
        "tanggal": tanggal_str,
        "kategori": kategori,
        "nominal": str(nominal),
        "pemasukan": str(pemasukan),
        "pengeluaran": str(pengeluaran)
    })

    save_data(data)
    print("Transaksi berhasil ditambahkan.\n")

def tampilkan_transaksi(data):
    print("\n--- Daftar Transaksi ---")
    for i, t in enumerate(data, start=1):
        print(f"{i}. {t['tanggal']} | {t['kategori']} | Rp{t['nominal']} | "
              f"{'Pemasukan' if int(t['pemasukan']) > 0 else 'Pengeluaran'}")
    print()

def ubah_transaksi(data):
    tampilkan_transaksi(data)
    idx = int(input("Masukkan nomor transaksi yang ingin diubah: ")) - 1
    if idx < 0 or idx >= len(data):
        print("Nomor tidak valid.\n")
        return

    t = data[idx]
    print("\n-- Ubah Data Transaksi --")
    tanggal_baru = input(f"Tanggal [{t['tanggal']}]: ") or t['tanggal']
    kategori_baru = input(f"Kategori [{t['kategori']}]: ") or t['kategori']
    nominal_input = input(f"Nominal [{t['nominal']}]: ") or t['nominal']
    nominal_baru = int(nominal_input)
    jenis_baru = input(f"Jenis (pemasukan/pengeluaran) [{'pemasukan' if int(t['pemasukan']) > 0 else 'pengeluaran'}]: ") or ('pemasukan' if int(t['pemasukan']) > 0 else 'pengeluaran')

    tahun_baru = tanggal_baru.split('-')[2]
    pemasukan_baru = nominal_baru if jenis_baru == "pemasukan" else 0
    pengeluaran_baru = nominal_baru if jenis_baru == "pengeluaran" else 0

    data[idx] = {
        "tahun": tahun_baru,
        "tanggal": tanggal_baru,
        "kategori": kategori_baru,
        "nominal": str(nominal_baru),
        "pemasukan": str(pemasukan_baru),
        "pengeluaran": str(pengeluaran_baru)
    }

    save_data(data)
    print("Transaksi berhasil diubah.\n")

def hapus_transaksi(data):
    tampilkan_transaksi(data)
    idx = int(input("Masukkan nomor transaksi yang ingin dihapus: ")) - 1
    if idx < 0 or idx >= len(data):
        print("Nomor tidak valid.\n")
        return

    konfirmasi = input(f"Yakin ingin menghapus transaksi ke-{idx+1}? (y/n): ")
    if konfirmasi.lower() == "y":
        del data[idx]
        save_data(data)
        print("Transaksi berhasil dihapus.\n")
    else:
        print("Penghapusan dibatalkan.\n")

def laporan_bulanan(data):
    bulan_input = input("Masukkan bulan (angka, misal 7): ")
    tahun_input = input("Masukkan tahun (misal 2025): ")

    print(f"\n📅 Laporan Bulanan - Bulan {bulan_input}, Tahun {tahun_input}")
    print("-" * 40)
    total_pemasukan = 0
    total_pengeluaran = 0

    for t in data:
        tgl = datetime.datetime.strptime(t['tanggal'], "%d-%m-%Y")
        if tgl.month == int(bulan_input) and t['tahun'] == tahun_input:
            print(f"{t['tanggal']} | {t['kategori']} | Rp{t['nominal']} | "
                  f"{'Pemasukan' if int(t['pemasukan']) > 0 else 'Pengeluaran'}")
            total_pemasukan += int(t['pemasukan'])
            total_pengeluaran += int(t['pengeluaran'])

    saldo = total_pemasukan - total_pengeluaran
    print("-" * 40)
    print(f"Total Pemasukan : Rp{total_pemasukan}")
    print(f"Total Pengeluaran : Rp{total_pengeluaran}")
    print(f"Saldo Akhir : Rp{saldo}\n")

def laporan_tahunan(data):
    tahun_input = input("Masukkan tahun (misal 2025): ")

    print(f"\n📅 Laporan Tahunan - Tahun {tahun_input}")
    print("-" * 40)
    total_pemasukan = 0
    total_pengeluaran = 0

    for t in data:
        if t['tahun'] == tahun_input:
            print(f"{t['tanggal']} | {t['kategori']} | Rp{t['nominal']} | "
                  f"{'Pemasukan' if int(t['pemasukan']) > 0 else 'Pengeluaran'}")
            total_pemasukan += int(t['pemasukan'])
            total_pengeluaran += int(t['pengeluaran'])

    saldo = total_pemasukan - total_pengeluaran
    print("-" * 40)
    print(f"Total Pemasukan : Rp{total_pemasukan}")
    print(f"Total Pengeluaran : Rp{total_pengeluaran}")
    print(f"Saldo Akhir : Rp{saldo}\n")

def menu():
    data = load_data()
    while True:
        print("=== Menu Transaksi Keuangan (CSV) ===")
        print("1. Tambah Transaksi")
        print("2. Tampilkan Daftar Transaksi")
        print("3. Ubah Transaksi")
        print("4. Hapus Transaksi")
        print("5. Laporan Bulanan")
        print("6. Laporan Tahunan")
        print("0. Keluar")
        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambah_transaksi(data)
        elif pilihan == "2":
            tampilkan_transaksi(data)
        elif pilihan == "3":
            ubah_transaksi(data)
        elif pilihan == "4":
            hapus_transaksi(data)
        elif pilihan == "5":
            laporan_bulanan(data)
        elif pilihan == "6":
            laporan_tahunan(data)
        elif pilihan == "0":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak valid.\n")

if _name_ == "_main_":
    menu()