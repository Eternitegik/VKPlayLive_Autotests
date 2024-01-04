import pytest
import Config

from src import WDWait, AdditionalFunctions

AuthorizedPassed = False


class TestAuthorized:

    def test_authorized(self, MainPage):
        '''301 | Проверка авторизации'''

        global AuthorizedPassed

        WDWait.VisibilityElement(
            MainPage, '//div[contains(@class, "TopMenuRightUnAuthorized_signIn")]', 'Кнопка авторизации не найдена').click()

        tabs = MainPage.window_handles
        MainPage.switch_to.window(tabs[1])

        login = WDWait.VisibilityElement(
            MainPage, '//input[@name="login"]', 'Не найдено поле для логина')

        login.send_keys(Config.USERLOGIN)

        passw = WDWait.VisibilityElement(
            MainPage, '//input[@name="password"]', 'Не найдено поле для пароля')

        passw.send_keys(Config.USERPASSWORD)

        WDWait.VisibilityElement(
            MainPage, '//button[@type="submit"]', 'Не найдена кнопка для авторизации').click()

        MainPage.switch_to.window(tabs[0])

        user_name = WDWait.VisibilityElement(
            MainPage, '//div[contains(@class, "ProfileMenu_name")]', 'Не найдено поле для имени')

        assert Config.USERNAME in user_name.text, 'Имя не соответствует шаблону'

        AuthorizedPassed = True

        AdditionalFunctions.SaveCookies(MainPage)

    @pytest.mark.parametrize(
        ('u_id', 'u_text', 'u_url', 'u_xpath'),
        [
            (0, 'Профиль VK Play', 'https://profile.vkplay.ru/profile/', 'a'),
            (1, 'Настройки профиля', 'https://account.vkplay.ru/profile/userinfo/', 'a'),
            (2, 'Настройки профиля Live', '/app/settings/edit', 'a'),
            (3, 'Служба поддержки', 'https://support.vkplay.ru/vkp_live', 'a'),
            (0, 'Мой канал', '', 'span'),
            (1, 'Студия', '', 'span'),
        ]
    )
    def test_profileMenu_dropdown(self, MainPage, u_id, u_text, u_url, u_xpath):
        '''302 | Проверка блока с меню профиля после авторизации'''

        if AuthorizedPassed == False:
            pytest.skip("Не пройдена авторизация")

        u_btn = WDWait.VisibilityElement(
            MainPage, '//div[contains(@class, "TopMenuRightAuthorized")]', 'Не найдена кнопка открытия меню пользователя')
        u_btn.click()

        a_buttons = WDWait.VisibilityElement_s(
            MainPage, f'//{u_xpath}[contains(@class, "ProfileMenuList_link")]')
        a_buttons_text = WDWait.VisibilityElement_s(
            MainPage, f'//{u_xpath}[contains(@class, "ProfileMenuList_link")]//div[contains(@class, "ProfileMenuItem_item")]')

        print(f'Проверка кнопки "{u_text}"')
        assert u_text in a_buttons_text[u_id].text
        if u_xpath == 'a':
            assert u_url in a_buttons[u_id].get_property('href')

        u_btn.click()
