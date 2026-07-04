import requests

def analyze_github_user(username):
    print(f"\n🔍 Собираю данные для пользователя: {username}...\n")
    
    # 1. Запрос информации о профиле
    user_url = f"https://api.github.com/users/{username}"
    user_resp = requests.get(user_url)
    
    if user_resp.status_code == 404:
        print("❌ Пользователь не найден. Проверь никнейм.")
        return
    elif user_resp.status_code != 200:
        print(f"❌ Ошибка GitHub API: {user_resp.status_code}")
        return
        
    user_data = user_resp.json()
    
    # Выводим базовую инфо
    print(f"👤 Имя: {user_data.get('name') or 'Не указано'}")
    print(f"📝 Био: {user_data.get('bio') or 'Пусто'}")
    print(f"👥 Подписчиков: {user_data.get('followers')} | Подписок: {user_data.get('following')}")
    print(f"📦 Публичных репозиториев: {user_data.get('public_repos')}")
    print("-" * 40)

    # 2. Запрос списка репозиториев
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    repos_resp = requests.get(repos_url)
    
    if repos_resp.status_code == 200:
        repos = repos_resp.json()
        
        if not repos:
            print("В репозиториях этого пользователя пока пусто.")
            return
            
        languages = {}
        print("📋 Последние проекты:")
        
        # Перебираем репозитории (максимум 5 для вывода на экран)
        for repo in repos[:5]:
            print(f" * {repo['name']} (⭐ Статусов: {repo['stargazers_count']})")
            
        # Считаем языки программирования
        for repo in repos:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1
                
        # Выводим статистику по языкам
        print("-" * 40)
        print("📊 Основные языки программирования пользователя:")
        sorted_langs = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        for lang, count in sorted_langs:
            print(f" - {lang}: использован в {count} репозиториях")
            
    else:
        print("Не удалось загрузить репозитории.")

if __name__ == "__main__":
    # Сюда можно вписать любой никнейм на GitHub
    # Например: 'torvalds' (создатель Linux) или твой собственный ник
    target_user = input("Введите никнейм на GitHub для анализа: ").strip()
    if target_user:
        analyze_github_user(target_user)