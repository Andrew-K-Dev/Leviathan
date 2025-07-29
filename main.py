from scrapers.scrape_ebay import scrape_ebay_listings
from pdf_bundler.create_info_product import generate_info_pdf

if __name__ == "__main__":
    data = scrape_ebay_listings()
    generate_info_pdf(data)