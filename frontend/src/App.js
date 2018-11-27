import React, { Component } from 'react';
import './App.css';
import Search from './Components/Search/Search';
import axios from 'axios';
import { API_URL } from './Config/api';
import CompanyInfo from './Components/CompanyInfo/CompanyInfo';
import { Container, Row, Jumbotron } from 'reactstrap';
import LatestQuote from './Components/LatestQuote/LatestQuote';

class App extends Component {
  state = {
    companyInfo: null,
    latestQuote: null,
  };

  fetchCompanyInfo = symbol => {
    axios
      .get(`${API_URL}/company/${symbol}`)
      .then(resp => this.setState({ companyInfo: resp.data }))
      .catch(error => console.log(error));
  };

  fetchLatestQuote = symbol => {
    axios
      .get(`${API_URL}/company/${symbol}/latest_quote/`)
      .then(resp => this.setState({ latestQuote: resp.data }))
      .catch(error => console.log(error));
  };

  fetchCompanyData = company => {
    const symbol = company[0] && company[0].symbol;

    if (!symbol) {
      return;
    }

    this.fetchCompanyInfo(symbol);
    this.fetchLatestQuote(symbol);
  };

  saveLatestQuote = quote => {
    const symbol = quote.symbol;

    return axios.post(`${API_URL}/company/${symbol}/save_quote/`, quote);
  };

  render() {
    return (
      <Container>
        <Jumbotron>
          <h1 className="display-3">Check my stocks quote!</h1>
          <p className="lead">
            This is a simple app that let's you see a stock quote for a given
            company
          </p>
          <hr className="my-2" />
          <Container>
            <Row>
              <Search onSelection={this.fetchCompanyData} />
            </Row>
            <Row>
              <div className="card-group mt-5 mr-3">
                <CompanyInfo info={this.state.companyInfo} />
                <LatestQuote
                  quote={this.state.latestQuote}
                  onSubmit={this.saveLatestQuote}
                />
              </div>
            </Row>
          </Container>
        </Jumbotron>
      </Container>
    );
  }
}

export default App;
