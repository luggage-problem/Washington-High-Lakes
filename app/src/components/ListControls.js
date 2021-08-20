
function ListControls({ searchText, setSearchText, setSearchCounty, setSearchOverabundant, setUserMapControl }) {
	return (
		<div className="ListControls">
			<table>
				<tbody>
				 	<tr>
				 		<td><button onClick={() => setUserMapControl(false)}>Reset Map Controls</button></td>
				 	</tr>
					<tr>
						<td>Search by name:</td>
						<td><input type="text" onChange={e => setSearchText(e.target.value)} value={searchText} /></td>
				 	</tr>
				 	<tr>
				 		<td>County:</td>
				 		<td>
							<select onChange={e => setSearchCounty(e.target.value)}>
								<option value="">Any</option>
								<option value="King">King County</option>
								<option value="Skamania">Skamania County</option>
								<option value="Okanogan">Okanogan County</option>
								<option value="Chelan">Chelan County</option>				
								<option value="Snohomish">Snohomish County</option>
								<option value="Skagit">Skagit County</option>
								<option value="Kittitas">Kittitas County</option>
								<option value="Yakima">Yakima County</option>
								<option value="Lewis">Lewis County</option>
								<option value="Whatcom">Whatcom County</option>
								<option value="Jefferson">Jefferson County</option>
								<option value="Pierce">Pierce County</option>
								<option value="Cowlitz">Cowlitz County</option>
								<option value="Harbor">Harbor County</option>
								<option value="Mason">Mason County</option>
								<option value="Clallam">Clallam County</option>
							</select>
						</td>
					</tr>
					<tr>
						<td>Overabundant:</td>
						<td>
							<select onChange={e => setSearchOverabundant(e.target.value)}>
								<option value="">Any</option>
								<option value="1">Yes</option>
								<option value="0">No</option>
							</select>
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	);
}

export default ListControls;