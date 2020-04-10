# AES
AES with CTR and CBC mode

truong trình thực hiện mã hóa AES với 2 mode là CTR và CBC

để sử dụng trương trình cần cài đặt 2 thu viện dó là pyaes và os (pyaes để sử dụng mã hóa khối AES thuần):
pip install pyaes
pip install os

để khởi tạo:
	aes = attt_aes.AES(key, iv)
	
	trong dó key và iv phải ở dạng byte (b''), có thể dùng attt_aes.random(size=16) để đọc chuỗi byte random của os
để mã hóa, có 2 mode:
	CBC - aes.encrypt_cbc(plaintext)
	      aes.decrypt_cbc(ciphertext)
	CBC - aes.encrypt_ctr(plaintext)
	      aes.decrypt_ctr(ciphertext)
	plaintex ở dạng str

chương trình bao có class AES bao gồm các phương thức:

	- contructor: nhận vào key và iv để gán vào biến lưu trữ

	- inc_bytes: nhận vào mảng byte và tăng giá trị của mảng byte thêm 1 đơn vị để phục vụ cho COUNTER MODE

	- strxor_bytes: nhận vào 2 mảng bytes để xor từng phần tử của 2 mảng với nhau (tham khảo code mẫu của thầy tại bài lập trình số 1)

	- PKCS_pad: nhận vào text và padding thêm để chia đủ thành các khối 16bytes theo PKCS#7
	hàm chia lấy dư độ dài text cho 16 và lấy 16 trừ đi giá trị đó để lấy số bytes cần pad mà giá trị pad

	- PKCS_unpad: nhận vào text và cắt đi phần pad của PKCS#7
	hàm lấy giá trị cuối cung của text, chuyển sang int và cắt đi từng đó byte của text(nếu phần cắt đi có phần tử k bằng giá trị pad thì sẽ báo lỗi)

	- split_16bytes và split_bytes: hàm nhận vào text và split theo các khối 16bytes và tra về mảng của các khối đó.
	đối với split_16bytes thì các khối bắt buộc phải 16bytes, còn split_bytes thì khối cuối cùng có thể nhỏ hơn 16bytes

	- encrypt_cbc: hàm nhận vào text và mã hóa AES theo CBC mode và trả về bản mã
	hàm thực hiện padding cho text, tiếp theo sẽ chia text thành các khối 16bytes
	với mỗi khối 16bytes hàm thực hiện chuyển khối đó thành mảng bytes để có thể xor với iv khi sử dụng hàm strxor_bytes
	xor iv với mảng bytes của block sau đó sử dụng mã hóa AES để được bản mã
	thay iv bằng block vừa được mã hóa và lặp lại
	gộp các bản mã của từng block lại và trả về bản đã mã hóa

	- decrypt_cbc: hàm nhận vào text và gải mã AES theo CBC mode
	hàm thực hiện chia text thành các khối 16bytes và chuyển các khối thành mảng bytes để có thể xor
	giải mã mảng bytes bằng giải mã AES sau đó xor vơi iv ta được bản rõ
	thay iv bằng mảng bytes được tách từ block 16bytes và lặp lại
	gộp các bản rõ lại ta được bản rõ ban đầu. thực hiện unpad PKCS#7 để lấy được bản rõ cuối cùng và trả về

	- encrypt_ctr: hàm nhận vào text và mã hóa AES theo CTR mode và trả về bản mã
	tiếp theo sẽ chia text thành các khối 16bytes (khối cuối có thể nhỏ hơn 16bytes)
	với mỗi khối 16bytes hàm thực hiện chuyển khối đó thành mảng bytes để có thể xor bằng strxor_bytes
	mã hóa iv với AES sau đó xor với mảng bytes phía trên ta được bản mã
	tăng iv thêm 1 bằng phương thức inc_bytes và lặp lại
	gộp các bản mã của từng block lại và trả về bản đã mã hóa

	- decrypt_ctr: hàm nhận vào text và gải mã AES theo CTR mode
	hàm thực hiện hoàn toàn giống với hàm encrypt_ctr nên em gọi luôn làm encrypt_ctr trong hàm decrypt_ctr
		
       
				     