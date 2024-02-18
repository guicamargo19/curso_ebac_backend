import time
import csv
import random
import concurrent.futures
import requests  # type: ignore
from bs4 import BeautifulSoup  # type: ignore

# global headers to be used for requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 \
            Safari/537.36 Edge/12.246'}

MAX_THREADS = 20


def extract_movie_details(movie_link):
    time.sleep(random.uniform(0, 0.2))
    response = BeautifulSoup(requests.get(
        movie_link, headers=headers).content, 'html.parser')
    movie_soup = response

    if movie_soup is not None:
        title = None
        date = None
        """ ajustar o trecho abaixo de acordo com o site de um filme, exemplo:
        https://www.imdb.com/title/tt15398776/?ref_=chtmvm_t_1,
        usar inspecionar elemento para definir os elementos. """
        movie_data = movie_soup.find('div', attrs={'sc-491663c0-3 bdjVSf'})
        if movie_data is not None:
            """ title é a span com classe de teste, é necessário acessar
            data-testid de h1 para ter seu acesso. """
            title = movie_data.find(
                'h1', attrs={'data-testid': 'hero__pageTitle'}) \
                .find('span').getText()  # type: ignore
            # date deve ser apenas a classe que representa o ano.
            date = movie_data.find('a', attrs={
                                   'class': 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'}).get_text().strip()
        # rating é a nota do filme, por exemplo, 8.6.
        rating = movie_soup.find('span', attrs={'sc-bde20123-1 cMEQkK'}).get_text() if movie_soup.find(
            'span', attrs={'sc-bde20123-1 cMEQkK'}) else None
        # plot é o texto de sinopse do filme
        plot_text = movie_soup.find('span', attrs={'class': 'sc-466bb6c-2 chnFO'}).get_text().strip() if movie_soup.find(
            'span', attrs={'class': 'sc-466bb6c-2 chnFO'}) else None

        with open('movies.csv', mode='a') as file:
            movie_writer = csv.writer(
                file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            if all([title, date, rating, plot_text]):
                print(title, date, rating, plot_text)
                movie_writer.writerow([title, date, rating, plot_text])


def extract_movies(soup):
    # aqui são configurações de hierarquia da página, do ponto de encontro do filme até sua divisão e organização em elementos.
    movies_table = soup.find(
        'div', attrs={'data-testid': 'chart-layout-main-column'}).find('ul')
    movies_table_rows = movies_table.find_all('li')
    movie_links = ['https://imdb.com' +
                   movie.find('a')['href'] for movie in movies_table_rows]

    threads = min(MAX_THREADS, len(movie_links))
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(extract_movie_details, movie_links)


def main():
    start_time = time.time()

    # IMDB Most Popular Movies - 100 movies
    popular_movies_url = 'https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm'
    response = requests.get(popular_movies_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies(soup)

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)


if __name__ == '__main__':
    main()
