const axios = require('axios');
const cheerio = require('cheerio');

const header = ["web-scraper-start-url", "Name", "Constellation", "Right ascension",
  "Declination", "Apparent magnitude", "Distance",
  "Proper motion RA", "Proper motion Dec", "B-T magnitude",
  "V-T magnitude", "Proper names", "HD",
  "TYCHO-2 2000", "USNO-A2.0", "BSC",
  "HIP"
];

async function getContent(url) {
  const examplePage = url;
  const { data } = await axios.get(examplePage, { responseType: 'document' })

  const $ = cheerio.load(data);

  const name = $('#d_body > h1').text();

  const firstTable = $('#d_body > table > tbody > tr > td:nth-child(2) > table:nth-child(4) > tbody').children().map((i, el) => ({
    key: $(el).find('td:nth-child(1)').text().replace(':', ''),
    value: $(el).find('td:nth-child(2)').text()
  })).get()

  const secondTable = $('#d_cat > tbody').children().map((i, el) => ({
    key: $(el).find('td:nth-child(1)').text(),
    value: $(el).find('td:nth-child(2)').text(),
  })).get();

  const allInfo = [
    { key: 'web-scraper-start-url', value: url },
    { key: 'Name', value: name },
    ...firstTable,
    ...secondTable
  ].filter(({ key, value }) => key !== '' && !key.includes('Request more') && !value.includes('(Edit)'));

  const object = Object.fromEntries(allInfo.map(({ key, value }) => [key, value]));

  const row = header.map((tag) => object[tag] ?? '');

  return row;
}


(async () => {
    const results = [header];
    const iterationSize = 10000;
    const from = iterationSize * (index - 1) + 201;
    const to = iterationSize * index + 201;
    console.log('start: ' + index);

    const objectIds = Array.from({ length: to - from }, (_, i) => i + from);

    const chunkSize = 400;

    const chunks = objectIds.reduce((acc, curr, i) => {
      const index = Math.floor(i / chunkSize);
      if (!acc[index]) {
        acc[index] = [];
      }
      acc[index].push(curr);
      return acc;
    }, []);



    let i = 0;
    for (const i in chunks) {
      const chunk = chunks[i];
      console.time('chunk: ' + i);
      const urls = chunk.map((i) => `https://server6.sky-map.org/starview?object_type=1&object_id=${i}&object_name=HD+1`);
      const rows = await Promise.all(urls.map((url) => getContent(url)));
      results.push(...rows);
      console.timeEnd('chunk: ' + i);
    }

    const fs = require('fs');
    fs.writeFileSync('data' + index + '.csv', results.map(item => item.join(',')).join('\n'), 'utf8');
})();