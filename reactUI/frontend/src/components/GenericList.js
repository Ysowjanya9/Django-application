import { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const useBaseUrl = () => {
  const [BASE_URL, setBaseUrl] = useState('');

  useEffect(() => {
    baseUrl();
  },[])

  const baseUrl = async () => {
    try {
      const ip = await fetch('/backendhost.txt');
      let host = (await ip.text()).trim();
      if (!host) {
        host = window.location.hostname;
      }
      const url = `${window.location.protocol}//${host}:8000/racing/api/`;
      setBaseUrl(url);
    } catch (err) {
      const fallback = `${window.location.protocol}//${window.location.hostname}:8000/racing/api`;
      setBaseUrl(fallback);
    }
  };
  return BASE_URL;
}

function GenericList({ model }) {
  const [items, setItems] = useState([]);
  const BASE_URL = useBaseUrl();
    
  useEffect(() => {
    if (!BASE_URL) return;
    fetchItems();
  }, [BASE_URL, model]);

  const API = {
    list: `${BASE_URL}${model}/`,
    delete: (id) => `${BASE_URL}${model}/delete/${id}/`,
  };

  const fetchItems = () => {
    axios.get(API.list)
      .then(res => setItems(res.data))
      .catch(err => console.error(err));
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure?")) return;
    try {
      const res = await axios.delete(API.delete(id));
      fetchItems();
      alert(res.data.message);
    } catch (err) {
      alert(err.response?.data?.message || "Error deleting.");
    }
  };

  return (
  <div>
    <h2 className="table-heading">{model.charAt(0).toUpperCase() + model.slice(1)}</h2>
    {items.length === 0 ? <p>No data available</p> : (
    <table border="1">
      <thead>
        <tr>
          {Object.keys(items[0]).map(k => <th key={k}>{k}</th>)}
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        {items.map(item => (
          <tr key={item.id}>
            {Object.keys(item).map(key => (
            <td key={key}>
              {key === 'logo_image' && item[key] ? (
                <a href={`${item[key]}`} target="_blank" rel="noopener noreferrer">Logo</a>
              ) : Array.isArray(item[key]) ? item[key].join(', ') : item[key]}
            </td>
            ))}
            <td>
              <Link to={`/${model}/edit/${item.id}`}>
              <button>Edit</button>
              </Link>
              <button onClick={() => handleDelete(item.id)}>Delete</button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
    )}
    <div className="create-buttons">
      <Link to={'/'}>
      <button>Home</button>
      </Link>
      <Link to={`/${model}/create`}>
      <button>Create</button>
      </Link>
    </div>
  </div>
  );
}

export {useBaseUrl, GenericList};
 