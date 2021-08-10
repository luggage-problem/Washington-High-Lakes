import React, { useState, useEffect } from 'react';
import { Fetch } from 'react-request';
import ListControls from './ListControls';
import List from './List';

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
			<ListControls setSearchText={setSearchText} setSearchCounty={setSearchCounty} setSearchOverabundant={setSearchOverabundant} />
			<List lakes={lakes} isLoaded={isLoaded} />
		</div>
	);
}

export default ListContainer;