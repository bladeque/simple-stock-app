import React from 'react';

import {
  Card,
  CardBody,
  CardTitle,
  Button,
  ListGroup,
  ListGroupItem,
  Alert,
  CardHeader,
} from 'reactstrap';

class LatestQuote extends React.Component {
  state = {
    message: null,
    buttonDisabled: false,
  };

  saveQuote = () => {
    const { quote, onSubmit } = this.props;

    onSubmit(quote).then(resp =>
      this.setState({ message: resp.data, buttonDisabled: true })
    );
  };

  render() {
    const { quote } = this.props;

    return (
      quote && (
        <div>
          <Card>
            <CardHeader>
              <CardTitle>Latest quote</CardTitle>
            </CardHeader>
            <CardBody>
              {this.state.message && (
                <Alert color="primary">{this.state.message}</Alert>
              )}
              <ListGroup className="mb-2">
                <ListGroupItem>Open: {quote.open}</ListGroupItem>
                <ListGroupItem>High: {quote.high}</ListGroupItem>
                <ListGroupItem>Low: {quote.low}</ListGroupItem>
                <ListGroupItem>Close: {quote.close}</ListGroupItem>
                <ListGroupItem>Price: {quote.price}</ListGroupItem>
                <ListGroupItem>Volume: {quote.volume}</ListGroupItem>
              </ListGroup>
              <Button
                color="primary"
                onClick={this.saveQuote}
                disabled={this.state.buttonDisabled}
              >
                Save
              </Button>
            </CardBody>
          </Card>
        </div>
      )
    );
  }
}

export default LatestQuote;
