- Project này tạo 1 pipeline để chuyển dữ liệu từ 1 postgreSQL ban đầu sang 1 postgreSQL khác. 
- Để sử dụng được postgreSQL thì cần pull image của postgreSQL về từ Docker Hub.
- Cách pipeline hoạt động:
    + Khởi tạo dữ liệu cho `source_db` bằng file `init.sql`, sau đó đổ nó vào file `data_dump.sql`, chuyển nó đến `destination_db` và load dữ liệu vào.
    + Sau đó sử dụng `dbt` để tạo 1 model/bảng mới dựa vào dữ liệu đã có trên `destination_db`. Dữ liệu mới này sẽ được lưu trữ trong 1 bảng mới trong `destination_db`.