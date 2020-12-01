import axios from 'axios'
import Cookies from 'universal-cookie';

export function ssget(url)
{
  let cookies = new Cookies();
  let api = cookies.get('api_switch');
  console.log('Going to request from ' + api);
  url = url.replace('http://api.studiosleepygiraffe.com/','http://api.studiosleepygiraffe.com/' + api + '/')
  console.log('URL: ' + url);
  return axios.get(url);
}
