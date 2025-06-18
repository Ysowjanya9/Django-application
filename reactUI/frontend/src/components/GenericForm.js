import { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useBaseUrl } from './GenericList';

// const hostname = window.location.hostname;
// const BASE_URL= `${window.location.protocol}//${hostname}:8000/racing/api/`;


const fieldConfig = {
  teams: [
    { name: 'team_name'},
    { name: 'city'},
    { name: 'country'},
    { name: 'logo_image', type: 'file'},
    { name: 'description'},
  ],
  drivers: [
    { name: 'first_name'},
    { name: 'last_name'},
    { name: 'date_of_birth', type: 'date' },
    { name: 'team', type: 'select', optionsKey: 'teams', optionLabel: 'team_name' },
  ],
  races: [
    { name: 'track_name'},
    { name: 'city'},
    { name: 'country'},
    { name: 'race_date', type: 'date' },
    { name: 'registration_closure_date', type: 'date' },
    { name: 'driver', type: 'multiselect', optionsKey: 'drivers', optionLabel: d => `${d.first_name} ${d.last_name}` },
  ],
};

function GenericForm({ model }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState({});
  const [teams, setTeams] = useState([]);
  const [drivers, setDrivers] = useState([]);
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(true);
  const BASE_URL = useBaseUrl();

  const API = {
    create: `${BASE_URL}${model}/create/`,
    edit: (id) => `${BASE_URL}${model}/edit/${id}/`,
  };

  useEffect(() => {
    console.log(BASE_URL);
    if (!BASE_URL) return;
    fetchData();
  }, [BASE_URL, id, model]);

  const fetchData = async () => {
    try {
      if (id) {
        const res = await axios.get(API.edit(id));
        const data = res.data;
        if (model === 'races' && Array.isArray(data.driver_names)) {
          const res = await axios.get(`${BASE_URL}/drivers/`);
          const drivers = res.data;
          setDrivers(drivers);
          const selectedIds = drivers.filter(d => data.driver_names.includes(`${d.first_name} ${d.last_name}`)).map(d => d.id);
          data.driver = selectedIds;
        }
        setForm(data);
      }
      if (model === 'drivers') {
        const res = await axios.get(`${BASE_URL}/teams/`);
        setTeams(res.data);
      } else if (model === 'races') {
        const res = await axios.get(`${BASE_URL}/drivers/`);
        setDrivers(res.data);
      }
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, files, multiple, options } = e.target;
    if (files) {
      setFile(files[0]);
    } else if (multiple) {
      setForm({ ...form, [name]: Array.from(options).filter(o => o.selected).map(o => (o.value)) });
    } else {
      setForm({ ...form, [name]: value === '' ? null : value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    Object.entries(form).forEach(([k, v]) => {
      if(k === 'logo_image') return;
      if (Array.isArray(v)) v.forEach(val => formData.append(k, val));
      else formData.append(k, v ?? '');
    });
    if (file) formData.append('logo_image', file);

    try {
      const method = model === 'teams' ? 'patch' : 'put';
      console.log(API.edit(id));
      id
        ? await axios[method](API.edit(id), formData)
        : await axios.post(API.create, formData);
      navigate(`/${model}`);
    } catch (err) {
      const errorData = err.response?.data || { error: ['An unexpected error occurred.'] };
      alert(
        Object.entries(errorData)
          .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
          .join('\n')
      );
    }
  };

  const renderField = ({ name, type, optionsKey, optionLabel }) => {
    const value = form[name] || '';
    const options = optionsKey === 'teams' ? teams : drivers;

    switch (type) {
      case 'file':
        return (
          <div key={name}>
            <label>{name}:</label>
            {form[name] && (
              <div>
                  <p>Currently: <a href={form[name]} target='_blank' rel='noopener noreferrer'>{form[name]}</a></p>
                  <p>Change:</p>
              </div>
              )}
            <input type="file" name={name} onChange={handleChange} />
          </div>
        );
      case 'select':
        return (
          <div key={name}>
            <label>{name}:</label>
            <select name={name} value={value} onChange={handleChange}>
              <option value="">-- Select --</option>
              {options.map(opt => (
                <option key={opt.id} value={opt[optionLabel]}>
                  {opt[optionLabel]}
                </option>
              ))}
            </select>
          </div>
        );
      case 'multiselect':
        return (
          <div key={name}>
            <label>{name}:</label>
            <select multiple name={name} value={form[name] || []} onChange={handleChange}>
              {options.map(opt => (
                <option key={opt.id} value={opt.id}>
                  {typeof optionLabel === 'function' ? optionLabel(opt) : opt[optionLabel]}
                </option>
              ))}
            </select>
          </div>
        );
      default:
        return (
          <div key={name}>
            <label>{name}:</label>
            <input type="text" name={name} value={value} onChange={handleChange} />
          </div>
        );
    }
  };
  if (loading) return <p>Loading...</p>;
  return (
    <form onSubmit={handleSubmit} encType="multipart/form-data">
      <h2>{id ? `Edit ${model.slice(0,-1)}` : `Create ${model.slice(0,-1)}`}</h2>
      {fieldConfig[model].map(renderField)}
      <Link to={`/${model}`}><button type="button" >Back</button></Link>
      <button type="submit">{id ? 'Update' : 'Create'}</button>
    </form>
  );
}

export default GenericForm;
