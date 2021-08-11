import React, { useState, useEffect } from 'react';
import ListControls from './ListControls';
import List from './List';

import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// I dunno about this whole react-leaflet thing... -> copied from https://github.com/PaulLeCam/react-leaflet/issues/453
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';
let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow
});
L.Marker.prototype.options.icon = DefaultIcon;
// 


function ListContainer() {

	const [lakes, setLakes] = useState([]);
	const [isLoaded, setIsLoaded] = useState(false);
	const [error, setError] = useState(null);
	const [searchText, setSearchText] = useState('');
	const [searchCounty, setSearchCounty] = useState('');
	const [searchOverabundant, setSearchOverabundant] = useState('');

	useEffect(() => {
		let query = '/api/lakes/?';
		if(searchText != '') {
			query += 'name=' + searchText + '&';
		}
		if(searchCounty != '') {
			query += 'county=' + searchCounty + '&';
		}
		if(searchOverabundant != '') {
			query += 'overabundant=' + searchOverabundant + '&';
		}
		fetch(query)
			.then(res => res.json())
			.then(
				(result) => {
					setIsLoaded(true);
					setLakes(result.results);
				},
				(error) => {
					setIsLoaded(true);
					setError(error);
				}
			)
	}, [searchText, searchCounty, searchOverabundant]);

	return (
		<div className="ListContainer">
			<MapContainer center={[47.3923, -121.4001]} zoom={6} className="mapContainer">
			  <TileLayer
			    attribution='&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
			    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
			  />
			  {lakes.map((lake) => 
				  <Marker position={[lake.lat, lake.long]} key={lake.id}>
				    <Popup>
				      {lake.name}
				    </Popup>
				  </Marker>
			  )}
			</MapContainer>
			<ListControls setSearchText={setSearchText} setSearchCounty={setSearchCounty} setSearchOverabundant={setSearchOverabundant} />
			<List lakes={lakes} isLoaded={isLoaded} />
		</div>
	);
}

export default ListContainer;