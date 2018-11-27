import React from 'react';
import { Card, CardBody, CardTitle, CardHeader } from 'reactstrap';

import './CompanyInfo.css';

const CompanyInfo = ({ info }) =>
  info && (
    <Card className="company-info">
      <CardHeader>
        <CardTitle>Company details</CardTitle>
      </CardHeader>
      <CardBody>
        <div className="media">
          {info.logo_url && (
            <img
              className="align-self-start mr-3"
              src={info.logo_url}
              alt="Company logo"
            />
          )}
          <div className="media-body">
            <h5 className="mt-0">{info.name}</h5>
            <p>Symbol: {info.symbol}</p>
            <p>
              Trading hours: {info.marketOpen} - {info.marketClose}
            </p>
            {info.url && (
              <p>
                Website:
                <a href={info.url} target="_blank" rel="noopener noreferrer">
                  link
                </a>
              </p>
            )}
          </div>
        </div>
      </CardBody>
    </Card>
  );

export default CompanyInfo;
