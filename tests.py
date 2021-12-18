import game
import pygame
import unittest


class GameTests(unittest.TestCase):
    def test_can_move(self):
        """
        Проверяем что персоонаж может перемещаться в пространстве (в частности по оси x)
        :return:
        """
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 255))
        boy = game.Player(game.fire_player, 'fire_p', game.water_sprite, 30, 30, 'live_fire', 270, 550)
        coord = boy.rect.topleft
        boy.speed[0] = 10
        for _ in range(5):
            boy.update()
        assert coord[0] != boy.rect.x

    def test_cant_move(self):
        """
        Проверяем что персонаж может упереться в стену и не сможет двигаться
        :return:
        """
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 255))
        boy = game.Player(game.fire_player, 'fire_p', game.water_sprite, 30, 30, 'live_fire', 270, 550)
        block_to_stand = game.Block(boy.rect.left, boy.rect.bottom, 'mud', game.blocks_group)
        block_to_block = game.Block(boy.rect.right, boy.rect.centery, 'mud', game.blocks_group)
        coord = boy.rect.topleft
        boy.speed[0] = 10
        for _ in range(5):
            boy.update()
        assert coord == boy.rect.topleft

    def test_lose_game(self):
        """
        Проверяем что при нулевом здоровье игра считается проигранной
        :return:
        """
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 255))
        boy = game.Player(game.fire_player, 'fire_p', game.water_sprite, 30, 30, 'live_fire', 270, 550)
        water = game.Liquid(270, 550, ['water', 'water_reverse'], game.water_sprite)
        for _ in range(3):
            boy.update()
        assert game.check_lose(boy.lives, 3) == 1

    def test_find_key(self):
        """
        Проверяет что при контакте с ключом персонажа, игра считает чт оон его нашёл
        :return:
        """
        size = width, height = 1280, 720
        screen = pygame.display.set_mode(size)
        screen.fill((0, 0, 255))
        boy = game.Player(game.fire_player, 'fire_p', game.water_sprite, 30, 30, 'live_fire', 270, 550)
        key = game.Key(270, 550, 'red_key', game.fire_key)
        boy.update()
        assert boy.find_key == True


if __name__ == '__name__':
    unittest.main()
