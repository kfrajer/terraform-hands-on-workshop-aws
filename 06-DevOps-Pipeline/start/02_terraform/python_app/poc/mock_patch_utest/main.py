import service 

def main():
    try:
        url = "http://www.example.com"
        result = service.get_data_from_api(url)
        print(f"Return from {url}:\n{result}")
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
