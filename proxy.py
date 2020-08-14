'' '
Tanggal: 15/3/2019
Penulis: Mohamed
Deskripsi: Membaca file yang berisi daftar proxy dan menentukan apakah daftar itu baik atau tidak.
             Setiap baris di file harus dalam format ip: port
'' '

platform impor
dari sistem impor os
dari waktu tidur impor
dari permintaan impor Sesi
dari Thread impor threading, RLock

proxy_list = 'proxies.txt'
target_site = 'https://instagram.com'


def get_proxies ():
    proxy = []

    dengan open (proxy_list, 'rt', encoding = 'utf-8') sebagai proxies_file:

        untuk baris di proxies_file:
            jika tidak baris:
                terus

            ip, port = line.replace ('\ r', '') .split (':')

            port = int (port)
            proxy = {'ip': ip, 'port': port}
            proxies.append (proxy)

    mengembalikan proxy


kelas TestProxies:

    def __init __ (diri, proxy):
        self.worked = 0
        self.failed = 0
        self.lock = RLock ()
        self.active_brs = 0
        self.is_alive = Benar
        self.proxies = proxy
        self.total = len (proxy)
        self.test_link = target_site

    tampilan def (diri):
        system ('cls' if platform.system () == 'Windows' else 'clear')
        berhasil, gagal, total = self.worked, self.failed, self.total

        working_per = round ((berhasil / total) * 100, 2)
        Fail_per = round ((gagal / total) * 100, 2)
        complete = round (berhasil_per + gagal_per, 2)

        cetak (f'Complete: {complete}% ')
        cetak (f'Active browser: {self.active_brs} ')
        cetak (f'Proxies bekerja: {working_per}% [{works}] ')
        cetak (f'Proxies gagal: {gagal_per}% [{gagal}] ')

    def test_proxy (diri, proxy):
        br = Sesi ()

        addr = '{}: {}'. format (proxy ['ip'], proxy ['port'])
        addr = {'http': addr, 'https': addr}
        br.proxies.update (addr)

        mencoba:
            br.get (self.test_link, timeout = (10, 15))

            dengan self.lock:
                self.worked + = 1
        kecuali:
            dengan self.lock:
                self.failed + = 1
        akhirnya:
            br.close ()

            jika self.is_alive:
                dengan self.lock:
                    self.display ()

            self.active_brs - = 1

    def mulai (sendiri):
        untuk proxy di self.proxies:

            sementara self.is_alive dan self.active_brs> = 512:
                lulus

            jika tidak self.is_alive:
                istirahat

            dengan self.lock:
                self.active_brs + = 1

            Thread (target = self.test_proxy, args = [proxy], daemon = True) .start ()

        sementara self.is_alive dan self.active_brs:
            tidur (0,5)

        self.display ()

    def stop (self):
        self.is_alive = Salah

        sementara self.active_brs:
            mencoba:
                dengan self.lock:
                    self.display ()

                tidur (0,5)
            kecuali KeyboardInterrupt:
                istirahat

    def memeriksa (diri):
        gagal = self.failed / self.total
        bekerja = self.worked / self.total

        jika berhasil == 0:
            print ('Daftar proxy buruk')
        elif (gagal - berhasil)> = 0,1:
            print ('Daftar proxy buruk')
        elif (gagal - berhasil) == 0:
            print ('Daftar proxy buruk')
        lain:
            print ('Daftar proxy yang baik')


jika __name__ == '__main__':
    test_proxies = TestProxies (get_proxies ())

    mencoba:
        test_proxies.start ()
    kecuali KeyboardInterrupt:
        test_proxies.stop ()
    akhirnya:
        test_proxies.examine ()