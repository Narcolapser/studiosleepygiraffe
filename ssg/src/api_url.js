import Cookies from 'universal-cookie';

export function api_url()
{
  let cookies = new Cookies();
  let api = cookies.get('api_switch');
  console.log('Going to request from ' + api);
  //let url = 'http://' + api + '.studiosleepygiraffe.com';
  let url = 'http://localhost:3001'
  console.log('URL: ' + url);
  return url
}
