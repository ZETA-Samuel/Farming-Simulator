import pygame

class Shop:

    def __init__(self,inventory):

        self.inventory = inventory

        self.font = pygame.font.Font(None, 28)
        self.small_font = pygame.font.Font(None, 22)
        self.title_font = pygame.font.Font(None, 42)

        self.items = [
            {"name": "Wheat Seeds", "price": 5},
            {"name": "Tomato Seeds", "price": 15},
        ]
        self.sell_prices = {
            "Wheat": 10,
            "Tomato": 20,
            "Wheat Seeds": 2,
            "Tomato Seeds": 7,
        }

        self.panel = pygame.Rect(0,0,700,430)
        self.panel.center = (pygame.display.get_surface().get_rect().center)

        self.close_button = pygame.Rect(self.panel.right - 45,self.panel.top + 15, 30,30)

        self.buy_buttons = []
        self.sell_buttons = []
        self.message = ""

    def handle_event(self, event):

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                return "close"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if self.close_button.collidepoint(event.pos):
                return "close"

            for button, item in self.buy_buttons:

                if button.collidepoint(event.pos):

                    success = self.inventory.buy(
                        item["name"],
                        item["price"])

                    if not success:
                        print("Not enough coins!")

                    break

            for button, item_name, price in self.sell_buttons:

                if button.collidepoint(event.pos):
                    if self.inventory.sell(item_name, price):
                        self.message = f"Sold {item_name} for {price} coins."
                    else:
                        self.message = f"No {item_name} to sell."

                    break

        return None

    def draw(self,surface):

        overlay = pygame.Surface(surface.get_size(),pygame.SRCALPHA)
        overlay.fill((0,0,0,150))
        surface.blit(overlay, (0,0))

        pygame.draw.rect(surface, (75,55,40),self.panel, border_radius=12)

        pygame.draw.rect(surface,(220,190,130),self.panel,4,border_radius=12) 

        title = self.title_font.render("FARM SHOP", True,(255,230,170))

        surface.blit(title, (self.panel.x + 25, self.panel.y + 15))

        pygame.draw.rect(surface,(160,60,60), self.close_button, border_radius=5)

        close_text = self.font.render("X", True,"white")

        surface.blit(close_text,close_text.get_rect(center=self.close_button.center))

        coins_text = self.font.render(f"Coins: {self.inventory.coins}", True, (255,220,70))

        surface.blit(coins_text, (self.panel.x + 25, self.panel.y + 65))

        pygame.draw.line(surface,(220,190,130),(self.panel.x + 340, self.panel.y + 60), (self.panel.x + 340, self.panel.bottom - 20), 2)

        shop_label = self.font.render("Available Items", True, "white")

        surface.blit(shop_label,(self.panel.x + 25,self.panel.y + 105))

        self.buy_buttons.clear()
        self.sell_buttons.clear()

        inventory_label = self.font.render("Your Inventory", True, "white")
        surface.blit(inventory_label, (self.panel.x + 365, self.panel.y + 105))

        for i, item in enumerate(self.items):
            y = self.panel.y + 150 + i * 48

            text = self.small_font.render(f'{item["name"]} - {item["price"]} coins', True, "white")

            surface.blit(text, (self.panel.x + 25, y + 8))

            button = pygame.Rect(self.panel.x + 270,y,55,32)

            pygame.draw.rect(surface,(80,145,75), button, border_radius=5)

            buy_text = self.small_font.render("Buy", True, "white")

            surface.blit(buy_text,buy_text.get_rect(center=button.center))

            self.buy_buttons.append((button, item))

        if not self.inventory.items:

            empty = self.small_font.render("Your inventory is empty", True,(200,200,200))
            surface.blit(empty, (self.panel.x + 365, self.panel.y + 150))

        else:
            for i, (name, quantity) in enumerate(self.inventory.items.items()):
                y = self.panel.y + 145 + i * 45
                price = self.sell_prices.get(name)
                item_label = f"{name} x{quantity}"
                if price is not None:
                    item_label += f" - {price} coins"
                text = self.small_font.render(item_label, True, "white")
                surface.blit(text, (self.panel.x + 365, y + 8))

                if price is not None:
                    button = pygame.Rect(self.panel.right - 85, y, 65, 32)
                    pygame.draw.rect(surface, (160, 90, 55), button, border_radius=5)
                    sell_text = self.small_font.render("Sell", True, "white")
                    surface.blit(sell_text, sell_text.get_rect(center=button.center))
                    self.sell_buttons.append((button, name, price))

        if self.message:
            message = self.small_font.render(self.message, True, (255, 220, 120))
            surface.blit(message, (self.panel.x + 25, self.panel.bottom - 35))
