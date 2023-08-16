from bs4 import BeautifulSoup
import requests
from pprint import pprint
import pandas as pd


def parse_product_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    description_tab = soup.find("div", id="tab-description")

    description = []
    for child_element in description_tab.findChildren(recursive=True):
        description.append(child_element.text)

    description = "".join(list(dict.fromkeys(description)))
    return description


def parse_shop_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    products = soup.find_all("div", class_="product-small box")

    for product in products:
        try:
            image_box = product.find("div", class_="box-image").find("div", class_="image-zoom")
            product_link = image_box.a.get('href')
            product_image_link = image_box.a.img.get('src')

            description_box = product.find("div", class_="box-text box-text-products")
            product_price = description_box.find("div", class_="price-wrapper").find("span", class_="price").text
            product_category = description_box.find("div", class_="title-wrapper").find("p", class_="category").text
            product_name = description_box.find("div", class_="title-wrapper").find("p", class_="name").text

            product_description = parse_product_page(product_link)

            product_map[product_name] = {
                "Loại Sản Phẩm": product_category,
                "Tên Sản Phẩm": product_name,
                "Giá Thành": product_price,
                "Mô Tả Đầy Đủ": product_description,
                "Link Sản Phẩm": product_link,
                "Link Ảnh": product_image_link
            }
        except Exception as ex:
            pprint(f"Error in parsing: {str(ex)}")
        finally:
            continue


if __name__ == "__main__":
    URLS = [
        "https://vinhhaphuxuyen.vn/shop/",
        "https://vinhhaphuxuyen.vn/shop/page/2/",
        "https://vinhhaphuxuyen.vn/shop/page/3/",
        "https://vinhhaphuxuyen.vn/shop/page/4/",
        "https://vinhhaphuxuyen.vn/shop/page/5/",
        "https://vinhhaphuxuyen.vn/shop/page/6/",
        "https://vinhhaphuxuyen.vn/shop/page/7/",
    ]

    product_map = {}

    for url in URLS:
        parse_shop_page(url)

    pprint(product_map)

    df = pd.DataFrame.from_dict(product_map, orient='index',
                       columns=["Loại Sản Phẩm","Tên Sản Phẩm","Giá Thành","Mô Tả Đầy Đủ","Link Sản Phẩm","Link Ảnh"])
    df.to_csv('vinh_ha_dataset.csv', index=False)
