import streamlit as st
import pandas as pd
import re
import os
import json
import time
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Tuple
import hashlib

# ==============================
# KELAS DASAR & ENKAPSULASI
# ==============================

class Mahasiswa:
    """Kelas untuk merepresentasikan data mahasiswa dengan enkapsulasi"""
    
    def __init__(self, nim: str, nama: str, jurusan: str = "Teknik Informatika"):
        self.__nim = nim  # Private attribute
        self.__nama = nama  # Private attribute
        self.__jurusan = jurusan  # Private attribute
    
    # Getter methods
    @property
    def nim(self) -> str:
        return self.__nim
    
    @property
    def nama(self) -> str:
        return self.__nama
    
    @property
    def jurusan(self) -> str:
        return self.__jurusan
    
    # Setter methods
    @nim.setter
    def nim(self, nim: str):
        if self._validasi_nim(nim):
            self.__nim = nim
        else:
            raise ValueError("NIM tidak valid")
    
    @nama.setter
    def nama(self, nama: str):
        if self._validasi_nama(nama):
            self.__nama = nama
        else:
            raise ValueError("Nama tidak valid")
    
    @jurusan.setter
    def jurusan(self, jurusan: str):
        self.__jurusan = jurusan
    
    # Validasi private methods
    def _validasi_nim(self, nim: str) -> bool:
        """Validasi NIM menggunakan regex"""
        pattern = r'^\d{9,12}$'
        return bool(re.match(pattern, nim))
    
    def _validasi_nama(self, nama: str) -> bool:
        """Validasi nama menggunakan regex"""
        pattern = r'^[A-Za-z\s\.\,]{3,50}$'
        return bool(re.match(pattern, nama))
    
    def to_dict(self) -> Dict:
        """Mengembalikan data mahasiswa sebagai dictionary"""
        return {
            'nim': self.__nim,
            'nama': self.__nama,
            'jurusan': self.__jurusan
        }
    
    def __str__(self) -> str:
        return f"{self.__nim} - {self.__nama} - {self.__jurusan}"

# ==============================
# INHERITANCE & POLYMORPHISM
# ==============================

class DataMahasiswa(ABC):
    """Abstract Base Class untuk manajemen data mahasiswa"""
    
    @abstractmethod
    def tambah(self, mahasiswa: Mahasiswa) -> bool:
        pass
    
    @abstractmethod
    def hapus(self, nim: str) -> bool:
        pass
    
    @abstractmethod
    def cari(self, keyword: str) -> List[Mahasiswa]:
        pass

class ManajemenMahasiswa(DataMahasiswa):
    """Kelas untuk mengelola data mahasiswa menggunakan array dan pointer"""
    
    def __init__(self):
        self.__data = []  # Private array untuk menyimpan data
        self.__pointer = 0  # Pointer untuk iterasi
    
    # Implementasi metode abstract
    def tambah(self, mahasiswa: Mahasiswa) -> bool:
        """Menambahkan mahasiswa ke dalam array"""
        try:
            # Cek duplikasi NIM
            for m in self.__data:
                if m.nim == mahasiswa.nim:
                    raise ValueError(f"Mahasiswa dengan NIM {mahasiswa.nim} sudah ada")
            
            self.__data.append(mahasiswa)
            return True
        except Exception as e:
            raise e
    
    def hapus(self, nim: str) -> bool:
        """Menghapus mahasiswa berdasarkan NIM"""
        for i, m in enumerate(self.__data):
            if m.nim == nim:
                del self.__data[i]
                return True
        return False
    
    def cari(self, keyword: str) -> List[Mahasiswa]:
        """Mencari mahasiswa berdasarkan keyword (NIM atau Nama)"""
        hasil = []
        for m in self.__data:
            if keyword.lower() in m.nim.lower() or keyword.lower() in m.nama.lower():
                hasil.append(m)
        return hasil
    
    # Metode tambahan
    def edit(self, nim_lama: str, mahasiswa_baru: Mahasiswa) -> bool:
        """Mengedit data mahasiswa"""
        for i, m in enumerate(self.__data):
            if m.nim == nim_lama:
                # Cek jika NIM baru sudah ada (kecuali NIM sama)
                if nim_lama != mahasiswa_baru.nim:
                    for m2 in self.__data:
                        if m2.nim == mahasiswa_baru.nim:
                            raise ValueError(f"Mahasiswa dengan NIM {mahasiswa_baru.nim} sudah ada")
                
                self.__data[i] = mahasiswa_baru
                return True
        return False
    
    def get_semua(self) -> List[Mahasiswa]:
        """Mengembalikan semua data mahasiswa"""
        return self.__data.copy()
    
    def get_by_nim(self, nim: str) -> Optional[Mahasiswa]:
        """Mengembalikan mahasiswa berdasarkan NIM"""
        for m in self.__data:
            if m.nim == nim:
                return m
        return None
    
    def jumlah(self) -> int:
        """Mengembalikan jumlah mahasiswa"""
        return len(self.__data)
    
    def __iter__(self):
        """Mengimplementasikan iterator"""
        self.__pointer = 0
        return self
    
    def __next__(self):
        """Mengembalikan elemen berikutnya dalam iterasi"""
        if self.__pointer < len(self.__data):
            result = self.__data[self.__pointer]
            self.__pointer += 1
            return result
        else:
            raise StopIteration

# ==============================
# ALGORITMA PENCARIAN
# ==============================

class AlgoritmaPencarian:
    """Kelas untuk implementasi berbagai algoritma pencarian"""
    
    @staticmethod
    def linear_search(data: List[Mahasiswa], keyword: str, by: str = 'nama') -> List[Mahasiswa]:
        """
        Linear Search - O(n)
        Mencari data secara sequential
        """
        hasil = []
        for m in data:
            if by == 'nama' and keyword.lower() in m.nama.lower():
                hasil.append(m)
            elif by == 'nim' and keyword in m.nim:
                hasil.append(m)
        return hasil
    
    @staticmethod
    def binary_search(data: List[Mahasiswa], nim: str) -> Optional[Mahasiswa]:
        """
        Binary Search - O(log n)
        Hanya bekerja pada data yang sudah terurut berdasarkan NIM
        """
        # Pastikan data terurut berdasarkan NIM
        data_sorted = sorted(data, key=lambda x: x.nim)
        
        low = 0
        high = len(data_sorted) - 1
        
        while low <= high:
            mid = (low + high) // 2
            if data_sorted[mid].nim == nim:
                return data_sorted[mid]
            elif data_sorted[mid].nim < nim:
                low = mid + 1
            else:
                high = mid - 1
        return None
    
    @staticmethod
    def sequential_search(data: List[Mahasiswa], keyword: str) -> List[Mahasiswa]:
        """
        Sequential Search - O(n)
        Variasi dari linear search
        """
        hasil = []
        i = 0
        n = len(data)
        
        while i < n:
            if keyword.lower() in data[i].nama.lower() or keyword in data[i].nim:
                hasil.append(data[i])
            i += 1
        return hasil

# ==============================
# ALGORITMA PENGURUTAN
# ==============================

class AlgoritmaPengurutan:
    """Kelas untuk implementasi berbagai algoritma pengurutan"""
    
    @staticmethod
    def bubble_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Bubble Sort - O(n²)
        Mengurutkan data dengan metode bubble sort
        """
        n = len(data)
        data_copy = data.copy()
        
        for i in range(n):
            for j in range(0, n - i - 1):
                if by == 'nim':
                    condition = data_copy[j].nim > data_copy[j + 1].nim if ascending else data_copy[j].nim < data_copy[j + 1].nim
                else:  # by == 'nama'
                    condition = data_copy[j].nama > data_copy[j + 1].nama if ascending else data_copy[j].nama < data_copy[j + 1].nama
                
                if condition:
                    data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
        
        return data_copy
    
    @staticmethod
    def selection_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Selection Sort - O(n²)
        Mengurutkan data dengan metode selection sort
        """
        n = len(data)
        data_copy = data.copy()
        
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if by == 'nim':
                    condition = data_copy[j].nim < data_copy[min_idx].nim if ascending else data_copy[j].nim > data_copy[min_idx].nim
                else:  # by == 'nama'
                    condition = data_copy[j].nama < data_copy[min_idx].nama if ascending else data_copy[j].nama > data_copy[min_idx].nama
                
                if condition:
                    min_idx = j
            
            data_copy[i], data_copy[min_idx] = data_copy[min_idx], data_copy[i]
        
        return data_copy
    
    @staticmethod
    def insertion_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Insertion Sort - O(n²)
        Mengurutkan data dengan metode insertion sort
        """
        data_copy = data.copy()
        
        for i in range(1, len(data_copy)):
            key = data_copy[i]
            j = i - 1
            
            while j >= 0:
                if by == 'nim':
                    condition = data_copy[j].nim > key.nim if ascending else data_copy[j].nim < key.nim
                else:  # by == 'nama'
                    condition = data_copy[j].nama > key.nama if ascending else data_copy[j].nama < key.nama
                
                if condition:
                    data_copy[j + 1] = data_copy[j]
                    j -= 1
                else:
                    break
            
            data_copy[j + 1] = key
        
        return data_copy
    
    @staticmethod
    def merge_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Merge Sort - O(n log n)
        Mengurutkan data dengan metode merge sort (rekursif)
        """
        if len(data) <= 1:
            return data.copy()
        
        mid = len(data) // 2
        left = AlgoritmaPengurutan.merge_sort(data[:mid], by, ascending)
        right = AlgoritmaPengurutan.merge_sort(data[mid:], by, ascending)
        
        return AlgoritmaPengurutan._merge(left, right, by, ascending)
    
    @staticmethod
    def _merge(left: List[Mahasiswa], right: List[Mahasiswa], by: str, ascending: bool) -> List[Mahasiswa]:
        """Helper method untuk merge sort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if by == 'nim':
                condition = left[i].nim < right[j].nim if ascending else left[i].nim > right[j].nim
            else:  # by == 'nama'
                condition = left[i].nama < right[j].nama if ascending else left[i].nama > right[j].nama
            
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    @staticmethod
    def shell_sort(data: List[Mahasiswa], by: str = 'nim', ascending: bool = True) -> List[Mahasiswa]:
        """
        Shell Sort - O(n log n) sampai O(n²)
        Mengurutkan data dengan metode shell sort
        """
        n = len(data)
        data_copy = data.copy()
        gap = n // 2
        
        while gap > 0:
            for i in range(gap, n):
                temp = data_copy[i]
                j = i
                
                while j >= gap:
                    if by == 'nim':
                        condition = data_copy[j - gap].nim > temp.nim if ascending else data_copy[j - gap].nim < temp.nim
                    else:  # by == 'nama'
                        condition = data_copy[j - gap].nama > temp.nama if ascending else data_copy[j - gap].nama < temp.nama
                    
                    if condition:
                        data_copy[j] = data_copy[j - gap]
                        j -= gap
                    else:
                        break
                
                data_copy[j] = temp
            gap //= 2
        
        return data_copy

# ==============================
# FILE I/O OPERATIONS
# ==============================

class FileHandler:
    """Kelas untuk menangani operasi file I/O"""
    
    @staticmethod
    def simpan_ke_file(data: List[Mahasiswa], filename: str = 'data_mahasiswa.json'):
        """Menyimpan data mahasiswa ke file JSON"""
        try:
            data_dict = [m.to_dict() for m in data]
            with open(filename, 'w') as file:
                json.dump(data_dict, file, indent=4)
            return True
        except Exception as e:
            raise Exception(f"Gagal menyimpan ke file: {str(e)}")
    
    @staticmethod
    def baca_dari_file(filename: str = 'data_mahasiswa.json') -> List[Mahasiswa]:
        """Membaca data mahasiswa dari file JSON"""
        try:
            if not os.path.exists(filename):
                return []
            
            with open(filename, 'r') as file:
                data_dict = json.load(file)
            
            data_mahasiswa = []
            for item in data_dict:
                try:
                    mahasiswa = Mahasiswa(
                        nim=item['nim'],
                        nama=item['nama'],
                        jurusan=item.get('jurusan', 'Teknik Informatika')
                    )
                    data_mahasiswa.append(mahasiswa)
                except Exception as e:
                    print(f"Error parsing data: {item} - {str(e)}")
            
            return data_mahasiswa
        except Exception as e:
            raise Exception(f"Gagal membaca dari file: {str(e)}")

# ==============================
# AUTHENTICATION SYSTEM
# ==============================

class AuthSystem:
    """Sistem autentikasi untuk login"""
    
    def __init__(self):
        self.__users = {
            'admin': self._hash_password('admin123'),
            'dosen': self._hash_password('dosen123'),
            'mahasiswa': self._hash_password('mahasiswa123')
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password menggunakan SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def login(self, username: str, password: str) -> bool:
        """Memvalidasi login"""
        if username in self.__users:
            return self.__users[username] == self._hash_password(password)
        return False

# ==============================
# STREAMLIT GUI APPLICATION
# ==============================

class AplikasiManajemenMahasiswa:
    """Kelas utama untuk aplikasi Streamlit"""
    
    def __init__(self):
        self.manajemen = ManajemenMahasiswa()
        self.auth = AuthSystem()
        self.file_handler = FileHandler()
        
        # Inisialisasi state session
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'data_mahasiswa' not in st.session_state:
            st.session_state.data_mahasiswa = []
        
        # Load data dari file saat aplikasi dimulai
        self._load_data()
    
    def _load_data(self):
        """Memuat data dari file"""
        try:
            data = self.file_handler.baca_dari_file()
            for m in data:
                self.manajemen.tambah(m)
            st.session_state.data_mahasiswa = self.manajemen.get_semua()
        except Exception as e:
            st.error(f"Error loading data: {str(e)}")
    
    def _save_data(self):
        """Menyimpan data ke file"""
        try:
            self.file_handler.simpan_ke_file(self.manajemen.get_semua())
        except Exception as e:
            st.error(f"Error saving data: {str(e)}")
    
    def login_page(self):
        """Halaman login"""
        # Custom CSS untuk halaman login
        st.markdown("""
        <style>
        .login-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            color: white;
        }
        .login-title {
            color: white;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 30px;
            font-weight: bold;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            border: 2px solid #ddd;
            padding: 10px;
            font-size: 16px;
        }
        .stButton>button {
            border-radius: 10px;
            padding: 10px 24px;
            font-size: 16px;
            font-weight: bold;
            transition: all 0.3s;
            width: 100%;
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
            border: none;
            color: white;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Layout login
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<h1 class="login-title">🔐 LOGIN</h1>', unsafe_allow_html=True)
            
            username = st.text_input("", placeholder="Username", key="login_user")
            password = st.text_input("", placeholder="Password", type="password", key="login_pass")
            
            # Tombol login dengan warna yang kontras
            if st.button("🚀 MASUK", use_container_width=True):
                if self.auth.login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.user_role = username
                    st.success("Login berhasil!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Username atau password salah!")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Info akun demo
            st.markdown("---")
            st.markdown("### 🔑 Akun Demo")
            
            cols = st.columns(3)
            with cols[0]:
                st.info("**Admin**\n\nUser: admin\nPass: admin123")
            with cols[1]:
                st.warning("**Dosen**\n\nUser: dosen\nPass: dosen123")
            with cols[2]:
                st.success("**Mahasiswa**\n\nUser: mahasiswa\nPass: mahasiswa123")
    
    def main_page(self):
        """Halaman utama aplikasi"""
        # Custom CSS untuk halaman utama
        st.markdown("""
        <style>
        /* Header dan judul */
        .main-header {
            background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%);
            padding: 20px;
            border-radius: 15px;
            color: white;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #2C3E50 0%, #34495E 100%);
        }
        
        [data-testid="stSidebar"] .stRadio > label {
            color: white !important;
            font-weight: 500;
            padding: 10px;
            border-radius: 8px;
            margin: 5px 0;
            transition: all 0.3s;
        }
        
        [data-testid="stSidebar"] .stRadio > label:hover {
            background: rgba(255,255,255,0.1);
            transform: translateX(5px);
        }
        
        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"] {
            background: transparent !important;
        }
        
        [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
            color: white !important;
            border-radius: 8px;
        }
        
        /* Tombol styling */
        .stButton > button {
            border-radius: 10px !important;
            padding: 12px 24px !important;
            font-weight: bold !important;
            transition: all 0.3s !important;
            border: none !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 6px 12px rgba(0,0,0,0.2) !important;
        }
        
        /* Primary button */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%) !important;
            color: white !important;
        }
        
        /* Secondary button */
        div[data-testid="stButton"] > button[kind="secondary"] {
            background: linear-gradient(135deg, #36D1DC 0%, #5B86E5 100%) !important;
            color: white !important;
        }
        
        /* Form container */
        [data-testid="stForm"] {
            border: 2px solid #E0E0E0 !important;
            border-radius: 15px !important;
            padding: 20px !important;
            background: white !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        }
        
        /* Metric cards */
        [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
            color: #2C3E50 !important;
        }
        
        .metric-card {
            background: white !important;
            padding: 20px !important;
            border-radius: 15px !important;
            border: 2px solid #E0E0E0 !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05) !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 10px 10px 0 0 !important;
            padding: 10px 20px !important;
            background-color: #F0F2F6 !important;
            border: 2px solid #E0E0E0 !important;
            border-bottom: none !important;
            font-weight: 500 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #4A00E0 0%, #8E2DE2 100%) !important;
            color: white !important;
            border-color: #4A00E0 !important;
        }
        
        /* Dataframe styling */
        .dataframe {
            border-radius: 10px !important;
            overflow: hidden !important;
            border: 2px solid #E0E0E0 !important;
        }
        
        /* Alert boxes */
        .stAlert {
            border-radius: 10px !important;
            border-left: 5px solid !important;
        }
        
        /* Success alert */
        [data-testid="stAlert"]:has(> div > div > div[role="alert"][style*="background-color: rgb(209, 250, 229)"]) {
            border-left-color: #10B981 !important;
        }
        
        /* Warning alert */
        [data-testid="stAlert"]:has(> div > div > div[role="alert"][style*="background-color: rgb(254, 252, 232)"]) {
            border-left-color: #F59E0B !important;
        }
        
        /* Error alert */
        [data-testid="stAlert"]:has(> div > div > div[role="alert"][style*="background-color: rgb(254, 226, 226)"]) {
            border-left-color: #EF4444 !important;
        }
        
        /* Info alert */
        [data-testid="stAlert"]:has(> div > div > div[role="alert"][style*="background-color: rgb(219, 234, 254)"]) {
            border-left-color: #3B82F6 !important;
        }
        
        /* Input fields */
        .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
            border-radius: 10px !important;
            border: 2px solid #E0E0E0 !important;
            padding: 10px !important;
            transition: all 0.3s !important;
        }
        
        .stTextInput>div>div>input:focus, .stSelectbox>div>div>div:focus, .stTextArea>div>div>textarea:focus {
            border-color: #4A00E0 !important;
            box-shadow: 0 0 0 3px rgba(74, 0, 224, 0.1) !important;
        }
        
        /* Radio buttons */
        .stRadio > div[role="radiogroup"] > label {
            background: #F8F9FA !important;
            border: 2px solid #E0E0E0 !important;
            border-radius: 10px !important;
            margin: 5px 0 !important;
            padding: 10px 15px !important;
        }
        
        .stRadio > div[role="radiogroup"] > label[data-baseweb="radio"]:has(input:checked) {
            background: linear-gradient(135deg, rgba(74, 0, 224, 0.1) 0%, rgba(142, 45, 226, 0.1) 100%) !important;
            border-color: #4A00E0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Header utama
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("🎓 SISTEM MANAJEMEN DATA MAHASISWA")
        with col2:
            user_badge = st.session_state.user_role.upper() if st.session_state.user_role else "GUEST"
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.2); padding: 10px; border-radius: 10px; text-align: center;">
                <strong>👤 {user_badge}</strong><br>
                <small>{self.manajemen.jumlah()} Mahasiswa</small>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Sidebar menu
        with st.sidebar:
            st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <h2 style="color: white; margin-bottom: 30px;">📋 MENU UTAMA</h2>
            </div>
            """, unsafe_allow_html=True)
            
            menu = st.radio(
                "",
                ["📊 Dashboard", "➕ Tambah Data", "✏️ Edit Data", "🗑️ Hapus Data", 
                 "🔍 Pencarian", "📈 Pengurutan", "ℹ️ Analisis Kompleksitas", "🚪 Logout"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            st.markdown("### 📊 Statistik")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total", self.manajemen.jumlah(), border=True)
            with col2:
                jurusan_count = {}
                for m in self.manajemen.get_semua():
                    jurusan_count[m.jurusan] = jurusan_count.get(m.jurusan, 0) + 1
                st.metric("Jurusan", len(jurusan_count), border=True)
            
            st.markdown("---")
            
            # Tombol aksi
            if st.button("💾 SIMPAN KE FILE", use_container_width=True, type="secondary"):
                with st.spinner("Menyimpan..."):
                    self._save_data()
                    st.success("✅ Data berhasil disimpan!")
            
            if st.button("🔄 MUAT ULANG DATA", use_container_width=True, type="secondary"):
                with st.spinner("Memuat..."):
                    self._load_data()
                    st.success("✅ Data berhasil dimuat ulang!")
        
        # Konten berdasarkan menu
        if menu == "📊 Dashboard":
            self._dashboard()
        elif menu == "➕ Tambah Data":
            self._tambah_data()
        elif menu == "✏️ Edit Data":
            self._edit_data()
        elif menu == "🗑️ Hapus Data":
            self._hapus_data()
        elif menu == "🔍 Pencarian":
            self._pencarian_data()
        elif menu == "📈 Pengurutan":
            self._pengurutan_data()
        elif menu == "ℹ️ Analisis Kompleksitas":
            self._analisis_kompleksitas()
        elif menu == "🚪 Logout":
            self._logout_page()
    
    def _dashboard(self):
        """Dashboard tampilan data"""
        st.header("📊 DASHBOARD DATA MAHASISWA")
        
        # Filter data
        with st.container(border=True):
            st.subheader("🔍 Filter Data")
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_nim = st.text_input("Cari NIM", placeholder="Masukkan NIM...")
            with col2:
                filter_nama = st.text_input("Cari Nama", placeholder="Masukkan nama...")
            with col3:
                filter_jurusan = st.selectbox(
                    "Filter Jurusan",
                    ["Semua Jurusan", "Teknik Informatika", "Sistem Informasi", 
                     "Teknik Komputer", "Manajemen Informatika", "Ilmu Komputer"]
                )
        
        # Tampilkan data
        data = self.manajemen.get_semua()
        
        # Filter data
        if filter_nim:
            data = [m for m in data if filter_nim in m.nim]
        if filter_nama:
            data = [m for m in data if filter_nama.lower() in m.nama.lower()]
        if filter_jurusan != "Semua Jurusan":
            data = [m for m in data if m.jurusan == filter_jurusan]
        
        if data:
            # Konversi ke DataFrame
            df_data = []
            for m in data:
                df_data.append({
                    'NIM': m.nim,
                    'Nama Lengkap': m.nama,
                    'Jurusan': m.jurusan
                })
            
            df = pd.DataFrame(df_data)
            
            # Tampilkan dengan container
            with st.container(border=True):
                st.subheader(f"📋 Data Mahasiswa ({len(data)} ditemukan)")
                st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Ekspor data
            st.markdown("---")
            st.subheader("📥 Ekspor Data")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📋 Salin ke Clipboard", use_container_width=True, type="secondary"):
                    st.code(df.to_string(index=False), language="text")
                    st.success("Data disalin ke clipboard!")
            with col2:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="💾 Download CSV",
                    data=csv,
                    file_name="data_mahasiswa.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with col3:
                json_data = json.dumps([m.to_dict() for m in data], indent=4)
                st.download_button(
                    label="📄 Download JSON",
                    data=json_data,
                    file_name="data_mahasiswa.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Tidak ada data mahasiswa yang ditemukan dengan filter tersebut.")
        
        # Statistik
        st.markdown("---")
        st.subheader("📈 Statistik Data")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Mahasiswa", len(data), border=True)
        with col2:
            if data:
                nim_terkecil = min(data, key=lambda x: x.nim).nim
                st.metric("NIM Terkecil", nim_terkecil, border=True)
        with col3:
            if data:
                nim_terbesar = max(data, key=lambda x: x.nim).nim
                st.metric("NIM Terbesar", nim_terbesar, border=True)
        with col4:
            jurusan_count = {}
            for m in data:
                jurusan_count[m.jurusan] = jurusan_count.get(m.jurusan, 0) + 1
            if jurusan_count:
                st.metric("Jurusan Terbanyak", max(jurusan_count, key=jurusan_count.get), border=True)
    
    def _tambah_data(self):
        """Form tambah data mahasiswa"""
        st.header("➕ TAMBAH DATA MAHASISWA BARU")
        
        with st.form("form_tambah", border=True):
            st.subheader("📝 Form Input Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                nim = st.text_input(
                    "**NIM** *",
                    placeholder="Contoh: 24101140099",
                    help="NIM harus 9-12 digit angka",
                    max_chars=12
                )
                nama = st.text_input(
                    "**Nama Lengkap** *",
                    placeholder="Contoh: Azka Insan Robbani",
                    help="Nama hanya boleh mengandung huruf, spasi, titik, dan koma",
                    max_chars=50
                )
            
            with col2:
                jurusan = st.selectbox(
                    "**Jurusan** *",
                    ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                     "Manajemen Informatika", "Ilmu Komputer"],
                    help="Pilih jurusan mahasiswa"
                )
                
                # Preview NIM
                if nim:
                    st.info(f"**Preview NIM:** `{nim}`")
            
            st.markdown("---")
            st.markdown("**📋 Format Valid:**")
            st.markdown("- ✅ NIM: 9-12 digit angka (24101140099)")
            st.markdown("- ✅ Nama: Huruf dan spasi saja (Azka Insan Robbani)")
            
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                submitted = st.form_submit_button(
                    "💾 SIMPAN DATA",
                    type="primary",
                    use_container_width=True
                )
            
            if submitted:
                try:
                    # Validasi input
                    if not nim or not nama:
                        st.error("❌ NIM dan Nama wajib diisi!")
                        return
                    
                    # Validasi regex untuk NIM
                    if not re.match(r'^\d{9,12}$', nim):
                        st.error("❌ NIM harus terdiri dari 9-12 digit angka!")
                        return
                    
                    # Validasi regex untuk Nama
                    if not re.match(r'^[A-Za-z\s\.\,]{3,50}$', nama):
                        st.error("❌ Nama hanya boleh mengandung huruf, spasi, titik, dan koma!")
                        return
                    
                    # Tambah data
                    mahasiswa_baru = Mahasiswa(nim=nim, nama=nama, jurusan=jurusan)
                    self.manajemen.tambah(mahasiswa_baru)
                    st.session_state.data_mahasiswa = self.manajemen.get_semua()
                    
                    st.success(f"✅ Data mahasiswa **{nama}** berhasil ditambahkan!")
                    st.balloons()
                    
                    # Reset form
                    time.sleep(2)
                    st.rerun()
                    
                except ValueError as e:
                    st.error(f"❌ Error: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Terjadi kesalahan: {str(e)}")
    
    def _edit_data(self):
        """Form edit data mahasiswa"""
        st.header("✏️ EDIT DATA MAHASISWA")
        
        # Pilih mahasiswa yang akan diedit
        data = self.manajemen.get_semua()
        if not data:
            st.info("ℹ️ Tidak ada data mahasiswa yang dapat diedit.")
            return
        
        with st.container(border=True):
            st.subheader("🔍 Pilih Mahasiswa")
            pilihan = {f"{m.nim} - {m.nama}": m.nim for m in data}
            selected = st.selectbox(
                "Pilih mahasiswa:",
                list(pilihan.keys()),
                placeholder="Pilih mahasiswa..."
            )
        
        if selected:
            nim_lama = pilihan[selected]
            mahasiswa = self.manajemen.get_by_nim(nim_lama)
            
            if mahasiswa:
                with st.form("form_edit", border=True):
                    st.subheader("📝 Edit Data")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nim_baru = st.text_input(
                            "**NIM Baru** *",
                            value=mahasiswa.nim,
                            max_chars=12,
                            help="NIM harus 9-12 digit angka"
                        )
                        nama_baru = st.text_input(
                            "**Nama Lengkap Baru** *",
                            value=mahasiswa.nama,
                            max_chars=50,
                            help="Nama hanya boleh mengandung huruf, spasi, titik, dan koma"
                        )
                    
                    with col2:
                        jurusan_baru = st.selectbox(
                            "**Jurusan Baru** *",
                            ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                             "Manajemen Informatika", "Ilmu Komputer"],
                            index=["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                                   "Manajemen Informatika", "Ilmu Komputer"].index(mahasiswa.jurusan)
                            if mahasiswa.jurusan in ["Teknik Informatika", "Sistem Informasi", "Teknik Komputer", 
                                                     "Manajemen Informatika", "Ilmu Komputer"]
                            else 0
                        )
                        
                        # Preview data lama
                        with st.expander("📋 Data Saat Ini"):
                            st.write(f"**NIM:** {mahasiswa.nim}")
                            st.write(f"**Nama:** {mahasiswa.nama}")
                            st.write(f"**Jurusan:** {mahasiswa.jurusan}")
                    
                    st.markdown("---")
                    
                    col1, col2, col3 = st.columns([2, 1, 2])
                    with col2:
                        submitted = st.form_submit_button(
                            "🔄 UPDATE DATA",
                            type="primary",
                            use_container_width=True
                        )
                    
                    if submitted:
                        try:
                            # Validasi input
                            if not nim_baru or not nama_baru:
                                st.error("❌ NIM dan Nama wajib diisi!")
                                return
                            
                            # Validasi regex untuk NIM
                            if not re.match(r'^\d{9,12}$', nim_baru):
                                st.error("❌ NIM harus terdiri dari 9-12 digit angka!")
                                return
                            
                            # Validasi regex untuk Nama
                            if not re.match(r'^[A-Za-z\s\.\,]{3,50}$', nama_baru):
                                st.error("❌ Nama hanya boleh mengandung huruf, spasi, titik, dan koma!")
                                return
                            
                            # Edit data
                            mahasiswa_baru = Mahasiswa(nim=nim_baru, nama=nama_baru, jurusan=jurusan_baru)
                            self.manajemen.edit(nim_lama, mahasiswa_baru)
                            st.session_state.data_mahasiswa = self.manajemen.get_semua()
                            
                            st.success("✅ Data mahasiswa berhasil diupdate!")
                            time.sleep(1)
                            st.rerun()
                            
                        except ValueError as e:
                            st.error(f"❌ Error: {str(e)}")
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {str(e)}")
    
    def _hapus_data(self):
        """Form hapus data mahasiswa"""
        st.header("🗑️ HAPUS DATA MAHASISWA")
        
        # Pilih mahasiswa yang akan dihapus
        data = self.manajemen.get_semua()
        if not data:
            st.info("ℹ️ Tidak ada data mahasiswa yang dapat dihapus.")
            return
        
        with st.container(border=True):
            st.subheader("🔍 Pilih Mahasiswa")
            pilihan = {f"{m.nim} - {m.nama}": m.nim for m in data}
            selected = st.selectbox(
                "Pilih mahasiswa yang akan dihapus:",
                list(pilihan.keys()),
                placeholder="Pilih mahasiswa..."
            )
        
        if selected:
            nim_hapus = pilihan[selected]
            mahasiswa = self.manajemen.get_by_nim(nim_hapus)
            
            if mahasiswa:
                # Konfirmasi hapus
                st.warning("""
                ⚠️ **PERHATIAN!** Anda akan menghapus data mahasiswa secara permanen.
                Aksi ini tidak dapat dibatalkan!
                """)
                
                with st.container(border=True):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("NIM", mahasiswa.nim)
                    with col2:
                        st.metric("Nama", mahasiswa.nama)
                    with col3:
                        st.metric("Jurusan", mahasiswa.jurusan)
                
                col1, col2, col3 = st.columns(3)
                with col2:
                    if st.button("🔥 HAPUS PERMANEN", type="primary", use_container_width=True):
                        try:
                            if self.manajemen.hapus(nim_hapus):
                                st.session_state.data_mahasiswa = self.manajemen.get_semua()
                                st.error(f"❌ Data mahasiswa **{mahasiswa.nama}** telah dihapus!")
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ Gagal menghapus data mahasiswa.")
                        except Exception as e:
                            st.error(f"❌ Terjadi kesalahan: {str(e)}")
    
    def _pencarian_data(self):
        """Halaman pencarian data"""
        st.header("🔍 PENCARIAN DATA MAHASISWA")
        
        # Input pencarian
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                keyword = st.text_input(
                    "Masukkan kata kunci pencarian:",
                    placeholder="Cari berdasarkan NIM atau Nama...",
                    help="Masukkan NIM (angka) atau nama mahasiswa"
                )
            with col2:
                st.write("")
                st.write("")
                if st.button("🔎 Cari", use_container_width=True, type="secondary"):
                    pass
        
        if keyword:
            data = self.manajemen.get_semua()
            
            # Tab untuk algoritma pencarian
            tab1, tab2, tab3 = st.tabs([
                "🔍 Linear Search", 
                "🎯 Binary Search", 
                "📋 Sequential Search"
            ])
            
            with tab1:
                st.subheader("Linear Search Algorithm")
                st.info("**⏱️ Time Complexity:** O(n)")
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    by = st.radio("Cari berdasarkan:", ["Nama", "NIM"], key="linear")
                
                start_time = time.time()
                hasil = AlgoritmaPencarian.linear_search(
                    data, keyword, by.lower()
                )
                end_time = time.time()
                
                if hasil:
                    st.success(f"✅ Ditemukan **{len(hasil)}** hasil ({end_time - start_time:.6f} detik)")
                    self._tampilkan_hasil_pencarian(hasil)
                else:
                    st.info("ℹ️ Tidak ditemukan hasil.")
            
            with tab2:
                st.subheader("Binary Search Algorithm")
                st.info("**⏱️ Time Complexity:** O(log n)")
                st.warning("⚠️ **Catatan:** Binary Search hanya bekerja pada data yang sudah terurut berdasarkan NIM")
                
                if re.match(r'^\d+$', keyword):
                    data_sorted = sorted(data, key=lambda x: x.nim)
                    
                    start_time = time.time()
                    hasil_binary = AlgoritmaPencarian.binary_search(data_sorted, keyword)
                    end_time = time.time()
                    
                    if hasil_binary:
                        st.success(f"✅ Ditemukan 1 hasil ({end_time - start_time:.6f} detik)")
                        self._tampilkan_hasil_pencarian([hasil_binary])
                    else:
                        st.info("ℹ️ Tidak ditemukan hasil.")
                else:
                    st.warning("⚠️ Binary Search hanya bisa mencari berdasarkan NIM (harus angka)")
            
            with tab3:
                st.subheader("Sequential Search Algorithm")
                st.info("**⏱️ Time Complexity:** O(n)")
                
                start_time = time.time()
                hasil_seq = AlgoritmaPencarian.sequential_search(data, keyword)
                end_time = time.time()
                
                if hasil_seq:
                    st.success(f"✅ Ditemukan **{len(hasil_seq)}** hasil ({end_time - start_time:.6f} detik)")
                    self._tampilkan_hasil_pencarian(hasil_seq)
                else:
                    st.info("ℹ️ Tidak ditemukan hasil.")
        else:
            st.info("ℹ️ Masukkan kata kunci di atas untuk memulai pencarian.")
    
    def _tampilkan_hasil_pencarian(self, hasil: List[Mahasiswa]):
        """Menampilkan hasil pencarian dalam tabel"""
        df_data = []
        for m in hasil:
            df_data.append({
                'NIM': m.nim,
                'Nama Lengkap': m.nama,
                'Jurusan': m.jurusan
            })
        
        df = pd.DataFrame(df_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _pengurutan_data(self):
        """Halaman pengurutan data"""
        st.header("📈 PENGURUTAN DATA MAHASISWA")
        
        with st.container(border=True):
            st.subheader("⚙️ Pengaturan Pengurutan")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                by = st.selectbox("Urutkan berdasarkan:", ["NIM", "Nama"])
            with col2:
                order = st.selectbox("Urutan:", ["Ascending (A-Z/0-9)", "Descending (Z-A/9-0)"])
            with col3:
                algorithm = st.selectbox(
                    "Algoritma Pengurutan:",
                    ["Bubble Sort", "Selection Sort", "Insertion Sort", 
                     "Merge Sort", "Shell Sort"]
                )
            
            if st.button("🚀 TERAPKAN PENGURUTAN", type="primary", use_container_width=True):
                data = self.manajemen.get_semua()
                ascending = order.startswith("Ascending")
                
                # Ukur waktu eksekusi
                with st.spinner(f"Menjalankan {algorithm}..."):
                    start_time = time.time()
                    
                    if algorithm == "Bubble Sort":
                        hasil = AlgoritmaPengurutan.bubble_sort(data, by.lower(), ascending)
                        complexity = "O(n²)"
                    elif algorithm == "Selection Sort":
                        hasil = AlgoritmaPengurutan.selection_sort(data, by.lower(), ascending)
                        complexity = "O(n²)"
                    elif algorithm == "Insertion Sort":
                        hasil = AlgoritmaPengurutan.insertion_sort(data, by.lower(), ascending)
                        complexity = "O(n²)"
                    elif algorithm == "Merge Sort":
                        hasil = AlgoritmaPengurutan.merge_sort(data, by.lower(), ascending)
                        complexity = "O(n log n)"
                    elif algorithm == "Shell Sort":
                        hasil = AlgoritmaPengurutan.shell_sort(data, by.lower(), ascending)
                        complexity = "O(n log n) sampai O(n²)"
                    
                    end_time = time.time()
                
                st.success(f"✅ Data berhasil diurutkan menggunakan **{algorithm}** ({complexity})")
                st.info(f"⏱️ **Waktu eksekusi:** {end_time - start_time:.6f} detik")
                
                # Tampilkan hasil
                df_data = []
                for m in hasil:
                    df_data.append({
                        'NIM': m.nim,
                        'Nama Lengkap': m.nama,
                        'Jurusan': m.jurusan
                    })
                
                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
    
    def _analisis_kompleksitas(self):
        """Halaman analisis kompleksitas algoritma"""
        st.header("ℹ️ ANALISIS KOMPLEKSITAS ALGORITMA")
        
        # Tab untuk informasi
        tab1, tab2 = st.tabs(["📊 Teori Kompleksitas", "🧪 Demo Perbandingan"])
        
        with tab1:
            st.subheader("📊 Perbandingan Time Complexity")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                ### 🔍 **Algoritma Pencarian**
                
                | Algoritma | Best Case | Average | Worst Case |
                |-----------|-----------|---------|------------|
                | **Linear** | O(1) | O(n) | O(n) |
                | **Binary** | O(1) | O(log n) | O(log n) |
                | **Sequential** | O(1) | O(n) | O(n) |
                
                ### 🎯 **Rekomendasi Pencarian**
                - Gunakan **Binary Search** jika data sudah terurut
                - Gunakan **Linear Search** untuk data tidak terurut
                - **Sequential Search** mirip dengan Linear Search
                """)
            
            with col2:
                st.markdown("""
                ### 📈 **Algoritma Pengurutan**
                
                | Algoritma | Best Case | Average | Worst Case |
                |-----------|-----------|---------|------------|
                | **Bubble Sort** | O(n) | O(n²) | O(n²) |
                | **Selection Sort** | O(n²) | O(n²) | O(n²) |
                | **Insertion Sort** | O(n) | O(n²) | O(n²) |
                | **Merge Sort** | O(n log n) | O(n log n) | O(n log n) |
                | **Shell Sort** | O(n log n) | O(n log n)² | O(n²) |
                
                ### 🏆 **Rekomendasi Pengurutan**
                - Data kecil: **Insertion Sort**
                - Data besar: **Merge Sort**
                - Pembelajaran: **Bubble Sort**
                """)
            
            st.markdown("---")
            st.subheader("📝 Konsep Dasar")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                with st.container(border=True):
                    st.markdown("### O(1)")
                    st.markdown("**Konstan**")
                    st.markdown("Operasi langsung selesai")
            
            with col2:
                with st.container(border=True):
                    st.markdown("### O(log n)")
                    st.markdown("**Logaritmik**")
                    st.markdown("Waktu bertambah sedikit meski data membesar")
            
            with col3:
                with st.container(border=True):
                    st.markdown("### O(n)")
                    st.markdown("**Linear**")
                    st.markdown("Waktu sebanding dengan jumlah data")
        
        with tab2:
            st.subheader("🧪 Demo Perbandingan Waktu Eksekusi")
            
            if st.button("▶️ JALANKAN PERBANDINGAN", type="primary", use_container_width=True):
                data = self.manajemen.get_semua()
                if len(data) < 5:
                    st.warning("⚠️ Minimal 5 data mahasiswa untuk perbandingan yang berarti.")
                    return
                
                # Buat data tes
                test_data = data.copy()
                
                results = []
                
                # Test sorting algorithms
                algorithms = [
                    ("Bubble Sort", AlgoritmaPengurutan.bubble_sort),
                    ("Selection Sort", AlgoritmaPengurutan.selection_sort),
                    ("Insertion Sort", AlgoritmaPengurutan.insertion_sort),
                    ("Merge Sort", AlgoritmaPengurutan.merge_sort),
                    ("Shell Sort", AlgoritmaPengurutan.shell_sort)
                ]
                
                progress_bar = st.progress(0)
                
                for idx, (algo_name, algo_func) in enumerate(algorithms):
                    progress_bar.progress((idx + 1) / len(algorithms), f"Menjalankan {algo_name}...")
                    
                    start_time = time.time()
                    algo_func(test_data, 'nim', True)
                    end_time = time.time()
                    
                    results.append({
                        'Algoritma': algo_name,
                        'Waktu (detik)': end_time - start_time,
                        'Data Points': len(test_data)
                    })
                
                progress_bar.empty()
                
                # Tampilkan hasil
                st.success("✅ Perbandingan selesai!")
                
                df_results = pd.DataFrame(results)
                df_results['Waktu (detik)'] = df_results['Waktu (detik)'].round(6)
                
                # Tabel hasil
                st.dataframe(df_results, use_container_width=True, hide_index=True)
                
                # Visualisasi
                st.subheader("📊 Grafik Perbandingan")
                st.bar_chart(
                    df_results.set_index('Algoritma')['Waktu (detik)']
                )
    
    def _logout_page(self):
        """Halaman logout"""
        st.header("🚪 LOGOUT")
        
        with st.container(border=True):
            st.warning("""
            ### ⚠️ Konfirmasi Logout
            
            Anda akan keluar dari sistem. Semua perubahan yang belum disimpan mungkin akan hilang.
            
            Pastikan Anda telah menyimpan data terlebih dahulu!
            """)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                if st.button("🔓 KONFIRMASI LOGOUT", type="primary", use_container_width=True):
                    st.session_state.logged_in = False
                    st.session_state.user_role = None
                    st.success("✅ Logout berhasil!")
                    time.sleep(1)
                    st.rerun()
                
                if st.button("↩️ BATAL", use_container_width=True, type="secondary"):
                    st.rerun()
    
    def run(self):
        """Menjalankan aplikasi"""
        st.set_page_config(
            page_title="Manajemen Data Mahasiswa",
            page_icon="🎓",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Routing berdasarkan status login
        if not st.session_state.logged_in:
            self.login_page()
        else:
            self.main_page()

# ==============================
# INISIALISASI DATA CONTOH
# ==============================

def inisialisasi_data_contoh():
    """Menginisialisasi data mahasiswa contoh"""
    data_contoh = [
        ("24101140099", "Azka Insan Robbani"),
        ("241011401958", "Bagus ardiansyah"),
        ("241011401713", "Fathur Rachman"),
        ("241011400087", "Tumpal Sinaga"),
        ("241011401650", "Vina Aulia"),
        ("241011400103", "Satria Apriza Fajar"),
        ("241011400085", "Davrielle saddad"),
        ("241012402295", "JANDRI HARTAT GEA"),
        ("241011400094", "Walman pangaribuan"),
        ("24011400075", "Rafli"),
        ("241011401866", "Jason Cornelius Chandra"),
        ("241011402663", "Ahmad Rasyid"),
        ("241011400068", "Ferda Ayi Sukaesih Sutanto"),
        ("241011402896", "M. Ikram Maulana"),
        ("241011400091", "Nazril Supriyadi"),
        ("241011402829", "Ade jahwa aulia"),
        ("241011400092", "Maulana ikhsan fadhillah"),
        ("241011400089", "Dea Amellya"),
        ("241011402427", "Risqi Eko Trianto"),
        ("241011400098", "Rizki Ramadani"),
        ("241011402197", "muhammad alif fajriansyah"),
        ("241011400097", "dzaki ramadhan"),
        ("241011400076", "Servatius Hasta Kristanto"),
        ("241011401761", "Ahmad Firdaus"),
        ("241011402338", "Ade sofyan"),
        ("241011402835", "Dimas Ahmad"),
        ("241011401470", "Adam Darmansyah"),
        ("241011400079", "Muhammad Noer Alam P"),
        ("241011403269", "Azmi Al Fahriza"),
        ("241011402053", "Ahmad Irfan"),
        ("241011402382", "Gregorius Gilbert Ieli Sarjana")
    ]
    
    return data_contoh

# ==============================
# MAIN EXECUTION
# ==============================

if __name__ == "__main__":
    try:
        # Buat instance aplikasi
        app = AplikasiManajemenMahasiswa()
        
        # Tambahkan data contoh jika file belum ada
        if not os.path.exists('data_mahasiswa.json'):
            data_contoh = inisialisasi_data_contoh()
            for nim, nama in data_contoh:
                try:
                    mahasiswa = Mahasiswa(nim=nim, nama=nama)
                    app.manajemen.tambah(mahasiswa)
                except Exception as e:
                    print(f"Error menambahkan {nama}: {str(e)}")
            
            # Simpan ke file
            app.file_handler.simpan_ke_file(app.manajemen.get_semua())
            print("✅ Data contoh berhasil dimuat!")
        
        # Jalankan aplikasi
        app.run()
        
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan fatal: {str(e)}")