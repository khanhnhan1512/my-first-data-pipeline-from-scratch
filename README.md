- Project này tạo 1 pipeline để chuyển dữ liệu từ 1 postgreSQL ban đầu sang 1 postgreSQL khác. 
- Để sử dụng được postgreSQL thì cần pull image của postgreSQL về từ Docker Hub.
- create db: docker exec -u postgres <container_name> createdb <db_name>
- connect db: docker exec -u postgres -it <container_name> psql <db_name>
- Cách pipeline hoạt động:
    + Khởi tạo dữ liệu cho `source_db` bằng file `init.sql`, sau đó đổ nó vào file `data_dump.sql`, chuyển nó đến `destination_db` và load dữ liệu vào.
    + Sau đó sử dụng `dbt` để tạo 1 model/bảng mới dựa vào dữ liệu đã có trên `destination_db`. Dữ liệu mới này sẽ được lưu trữ trong 1 bảng mới trong `destination_db`.
    + `Cron` job sẽ chạy file `elt_script.sh` để tự động hóa quá trình này.
    + Hoặc thay vào đó sử dụng `airflow`.
    + `airbyte` sẽ giúp chuyển đổi và đồng bộ hóa dữ liệu giữa `source_db` và `destination_db` thay vì sử dụng script `elt_script.py`.