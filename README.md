# Car Collection App


## Run API as Gunicorn Service
1. Install Gunicorn
    ```
    sudo apt-get update
    ```
    ```
    sudo apt-get install gunicorn
    ```
2. Create new service file name `car-collection-api.service` in path `/etc/systemd/system/`
    ```
    touch /etc/systemd/system/car-collection-api.service
    ```
3. Open the file as super user
    ```
    sudo nano /etc/systemd/system/car-collection-api.service
    ```
4. Paste this configuration. Change `User` with your device hostname, `WorkingDirectory` with your directory to api file, and `Execstart` with the path to gunicorn executable file.
    ```
    [Unit]
    Description=Car Collection API Gunicorn Service
    After=network.target

    [Service]
    Type=simple
    # the specific user that our service will run as
    User=YOUR_HOSTNAME
    # Directory to the api file script --DIRECTORY ONLY NO NEED THE FILE NAME--
    WorkingDirectory=/YOUR/PATH/TO/API/SCRIPT/DIRECTORY/
    ExecStart=/PATH/TO/GUNICORN/gunicorn --bind 0.0.0.0:5000 --workers 4 Api:run()
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
5. Save and close the configuration file
6. Reload the systemd file
    ```
    sudo systemctl daemon-reload
    ```
7. Start the service
    ```
    sudo systemctl start car-collection-api.service
    ```