from bs4 import BeautifulSoup
import requests
import csv
from urllib.parse import urljoin


class Book:
    def __init__(self, title, price, rating, availability):
        self.title = title
        self.price = price          # float
        self.rating = rating        # int (1–5)
        self.availability = availability


class BookScraper:
    BASE_URL = "https://books.toscrape.com/catalogue/"
    START_URL = "https://books.toscrape.com/catalogue/page-1.html"

    def __init__(self):
        self.session = requests.Session()

    def convert_rating(self, rating_text):
        """
        Convert rating text into integer.
        Example:
        'star-rating Three' -> 3
        """

        rating_map = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
        }

        for word, number in rating_map.items():
            if word in rating_text:
                return number

        return 0

    def scrape_page(self, soup) -> list[Book]:
        """
        Scrape all books from a single page soup.
        """

        books_data = []

        books = soup.find_all(
            "article",
            class_="product_pod"
        )

        for book in books:

            # -----------------------------
            # TITLE
            # -----------------------------
            title = book.h3.a["title"].strip()

            # -----------------------------
            # PRICE
            # -----------------------------
            price_text = book.find(
                "p",
                class_="price_color"
            ).text.strip()

            # Remove £ symbol and convert to float
            price = float(
                price_text.replace("£", "")
            )

            # -----------------------------
            # RATING
            # -----------------------------
            rating_classes = book.find(
                "p",
                class_="star-rating"
            )["class"]

            rating_text = " ".join(rating_classes)

            rating = self.convert_rating(
                rating_text
            )

            # -----------------------------
            # AVAILABILITY
            # -----------------------------
            availability = book.find(
                "p",
                class_="instock availability"
            ).text.strip()

            # -----------------------------
            # CREATE BOOK OBJECT
            # -----------------------------
            book_object = Book(
                title,
                price,
                rating,
                availability
            )

            books_data.append(book_object)

        return books_data

    def get_next_page(self, soup) -> str | None:
        """
        Return next page URL if it exists.
        """

        next_button = soup.find(
            "li",
            class_="next"
        )

        if next_button:

            relative_url = next_button.a["href"]

            return urljoin(
                self.BASE_URL,
                relative_url
            )

        return None

    def scrape_all(self) -> list[Book]:
        """
        Scrape all pages from the website.
        """

        all_books = []

        current_url = self.START_URL

        while current_url:

            print(f"Scraping: {current_url}")

            try:
                # -----------------------------
                # SINGLE REQUEST PER PAGE
                # -----------------------------
                response = self.session.get(
                    current_url
                )

                response.raise_for_status()

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                # -----------------------------
                # SCRAPE CURRENT PAGE
                # -----------------------------
                page_books = self.scrape_page(
                    soup
                )

                all_books.extend(
                    page_books
                )

                # -----------------------------
                # GET NEXT PAGE
                # -----------------------------
                current_url = self.get_next_page(
                    soup
                )

            except requests.RequestException as e:
                print(f"Request error: {e}")
                break

        return all_books

    def save_to_csv(self, books, filename):
        """
        Save books to CSV using csv module.
        """

        with open(
            filename,
            mode="w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            # Header row
            writer.writerow([
                "Title",
                "Price",
                "Rating",
                "Availability"
            ])

            # Data rows
            for book in books:

                writer.writerow([
                    book.title,
                    book.price,
                    book.rating,
                    book.availability
                ])

        print(f"CSV saved as '{filename}'")


def main():

    scraper = BookScraper()

    books = scraper.scrape_all()

    scraper.save_to_csv(
        books,
        "books.csv"
    )

    print(
        f"Done. {len(books)} books saved."
    )


if __name__ == "__main__":
    main()
