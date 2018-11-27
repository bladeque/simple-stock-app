import React from 'react';
import axios from 'axios';

import { AsyncTypeahead } from 'react-bootstrap-typeahead';
import { API_URL } from '../../Config/api';

// TODO: add prop types

class Search extends React.Component {
  state = {
    isLoading: false,
    options: [],
    selected: null,
  };

  render() {
    const { onSelection } = this.props;

    return (
      <AsyncTypeahead
        {...this.state}
        labelKey="name"
        filterBy={['symbol']}
        minLength={2}
        onSearch={this._handleSearch}
        placeholder="Put company symbol here"
        onChange={onSelection}
      />
    );
  }

  _handleSearch = query => {
    this.setState({ isLoading: true });
    // TODO: strip the query

    axios
      .get(`${API_URL}/search`, {
        params: {
          query,
        },
      })
      .then(this._handleResponse)
      .catch(error => console.log(error));
  };

  _handleResponse = response => {
    this.setState({ isLoading: false, options: response.data });
  };
}

export default Search;
