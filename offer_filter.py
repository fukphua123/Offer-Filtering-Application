import argparse
import json
from datetime import datetime, timedelta
from typing import List, Dict, Union

class Category:
    def __init__(self, category_id: int, name: str):
        self.id = category_id
        self.name = name
class CategoryFilter:
    def __init__(self, categories: List[Category]):
        self.categories = {category.id: category for category in categories}

    def find_category_by_id(self, category_id: int) -> Category:
        return self.categories.get(category_id, None)
    
class Offer:
    def __init__(self, offer_id: int, title: str, description: str, category: Category, merchants: List[Dict[str, Union[int, str, float]]], valid_to: str):
        self.id = offer_id
        self.title = title
        self.description = description
        self.category = category
        self.merchants = [Merchant(**merchant_data) for merchant_data in merchants]
        self.valid_to = datetime.strptime(valid_to, '%Y-%m-%d') if self.is_valid_date(valid_to) else None

    def is_valid_date(self, date_string: str) -> bool:
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def is_valid(self, check_in_date: datetime) -> bool:
        return self.valid_to is not None and check_in_date + timedelta(days=5) <= self.valid_to 
    def get_closest_merchant(self) -> 'Merchant':
        return min(self.merchants, key=lambda merchant: merchant.distance)

    def to_dict(self) -> Dict[str, Union[int, str, List[Dict[str, Union[int, str, float]]], str]]:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category.id,
            'merchants': [self.get_closest_merchant().to_dict()],
            'valid_to': self.valid_to.strftime('%Y-%m-%d') if self.valid_to else None
        }

class Merchant:
    def __init__(self, id: int, name: str, distance: float):
        self.id = id
        self.name = name
        self.distance = distance

    def to_dict(self) -> Dict[str, Union[int, str, float]]:
        return {
            'id': self.id,
            'name': self.name,
            'distance': self.distance
        }

class OffersFilter:
    def __init__(self, check_in_date: str):
        self.check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d')
        self.offers = []
        self.offersCount = 2
        self.max_offers_per_category = 1  # Variable to limit offers to 1 per category
        self.limit_categories = {1,2,4}
        
    def load_categories(self) -> CategoryFilter:
       
        categories_list = [
            Category(category_id=1, name="Restaurant"),
            Category(category_id=2, name="Retail"),
            Category(category_id=3, name="Hotel"),
            Category(category_id=4, name="Activity"),
        ]

        
        category_filter = CategoryFilter(categories_list)
        return category_filter
    

    def load_from_json(self, file_path: str ) -> None:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)['offers']
                category_filter = self.load_categories()
                for offer_data in data:
                    category = category_filter.find_category_by_id(offer_data['category'])
                    offer = Offer(offer_data['id'], offer_data['title'], offer_data['description'],
                                  category, offer_data['merchants'], offer_data['valid_to'])
                    self.offers.append(offer)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading from JSON file: {e}")

    def filter_offers(self) -> List[Offer]:
        selected_offers = []
        selected_categories = set()

        category_groups = {}
        for offer in self.offers:
            if offer.is_valid(self.check_in_date) and offer.category.id in self.limit_categories:
                if offer.category.id not in category_groups:
                    category_groups[offer.category.id] = []
                category_groups[offer.category.id].append(offer)

        for category_id, offers in sorted(category_groups.items(), key=lambda x: x[1][0].get_closest_merchant().distance):
            if len(selected_offers) >= min(self.offersCount,self.max_offers_per_category * len(self.limit_categories)):
                break

            if offers:
                closest_merchant_offer = min(offers, key=lambda offer: offer.get_closest_merchant().distance)

                if category_id not in selected_categories:
                    selected_offers.append(closest_merchant_offer)
                    selected_categories.add(category_id)

        return selected_offers

    def save_to_json(self, output_file_path: str, filtered_offers: List[Offer]) -> None:
        try:
            filtered_data = [offer.to_dict() for offer in filtered_offers]
            with open(output_file_path, 'w') as file:
                json.dump({"offers": filtered_data}, file, indent=2)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error saving to JSON file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Filter offers based on certain criteria.')
    parser.add_argument('check_in_date', help='Check-in date (YYYY-MM-DD)')
   # parser.add_argument('input_file_path', help='Input JSON file path')
   # parser.add_argument('output_file_path', help='Output JSON file path')
    args = parser.parse_args()
    file_path = "input.json"
    output_file_path = "output.json"
    offers_filter = OffersFilter(args.check_in_date)
    offers_filter.load_from_json(file_path)
    filtered_offers = offers_filter.filter_offers()
    offers_filter.save_to_json(output_file_path,filtered_offers)

if __name__ == "__main__":
    main()
