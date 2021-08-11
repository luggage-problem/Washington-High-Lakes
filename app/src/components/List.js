
function List({ lakes, isLoaded }) {
	if(!isLoaded) {
		return (
			<div className="List">
				loading...
			</div>
		);
	} else {
		return (
			<table className="List">
				<thead>
					<tr>
						<td>Name</td>
						<td>County</td>
						<td>Elevation</td>
						<td>Area</td>
					</tr>
				</thead>
				<tbody>
					{lakes.map((lake, index) => (
						<tr key={lake.id}>
							<td>{lake.name}</td>
							<td>{lake.county}</td>
							<td>{lake.elevation} ft.</td>
							<td>{lake.area} acres</td>
						</tr>
					))}
				</tbody>
			</table>
		);
	}
}

export default List;