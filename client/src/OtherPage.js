import React, { Component } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

class Test extends Component {
  state = {
    seenIndexes: [],
    values: {},
    index: "asdf",
  };
  componentDidMount() {
    this.fetchValues();
    // this.fetchIndexes();
  }
  async fetchValues() {
    // const config = {
    //   headers: {
    //     "Content-Type": "application/json",
    //     Accept: "application/json",
    //   },
    // };
    // const values = await axios.get("http://localhost:5000/product/all", config);
    const values = await axios.get("http://localhost:5000/product/all");

    console.log(values.data);
    this.setState({ index: values.data });
  }

  render() {
    return (
      <div>
        <h3>Indexes I have seen:</h3>
        {this.state.index}
        <Link to="/">Go back home</Link>
      </div>
    );
  }
}
export default Test;
