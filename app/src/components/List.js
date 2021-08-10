
function List({ lakes, isLoaded }) {
	if(!isLoaded) {
		return (
			<div className="List">
				loading...
			</div>
		);
	} else {
		return (
			<div className="List">
				<ul>
				{lakes.map((lake, index) => (
					<li key={lake.id}>{lake.name}</li>
				))}
				</ul>
			</div>
		);
	}
}

export default List;