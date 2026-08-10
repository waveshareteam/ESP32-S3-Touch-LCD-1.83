from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HERO = "assets/images/ESP32-S3-Touch-LCD-1.83.jpg"
MODEL = "ESP32-S3-Touch-LCD-1.83"
PRODUCT_URL = "https://www.waveshare.com/product/esp32-s3-touch-lcd-1.83.htm"
IMAGE_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
ATTRIBUTE = re.compile(r'''\b(?P<name>src|alt)="(?P<value>[^"]*)"''', re.IGNORECASE)


class HomepageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.homepages = {
            path: (ROOT / path).read_text(encoding="utf-8")
            for path in ("README.md", "README_ZH.md")
        }

    def test_homepages_share_the_local_product_hero(self) -> None:
        hero_path = (ROOT / HERO).resolve()
        self.assertTrue(hero_path.is_relative_to(ROOT.resolve()))
        self.assertTrue(hero_path.is_file())
        self.assertEqual(b"\xff\xd8\xff", hero_path.read_bytes()[:3])

        for homepage, text in self.homepages.items():
            heroes = []
            for tag in IMAGE_TAG.findall(text):
                attributes = {match["name"].lower(): match["value"] for match in ATTRIBUTE.finditer(tag)}
                if attributes.get("src") == HERO:
                    heroes.append(attributes)
            self.assertEqual(1, len(heroes), homepage)
            self.assertTrue(heroes[0].get("alt"), homepage)
            self.assertIn(MODEL, heroes[0]["alt"], homepage)

    def test_homepages_link_to_the_official_product_page(self) -> None:
        for homepage, text in self.homepages.items():
            self.assertIn(PRODUCT_URL, text, homepage)

    def test_configuration_preserves_single_product_homepage_contract(self) -> None:
        markdown_config = json.loads((ROOT / "config/markdown-audit.json").read_text(encoding="utf-8"))
        homepage_pair = next(
            pair
            for pair in markdown_config["homepage_pairs"]
            if pair["english"] == "README.md" and pair["chinese"] == "README_ZH.md"
        )
        self.assertEqual("single-product", homepage_pair["profile"])
        self.assertIn("hero_image", homepage_pair["required_components"])
        self.assertIn("product", homepage_pair["required_quick_links"])
        self.assertIn(HERO, markdown_config["docs_only_allowed_patterns"])

        routing_config = json.loads((ROOT / "config/ci-routing.json").read_text(encoding="utf-8"))
        self.assertIn(HERO, routing_config["documentation_asset_patterns"])


if __name__ == "__main__":
    unittest.main()
