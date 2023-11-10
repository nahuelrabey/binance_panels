import { LineStyle } from "lightweight-charts";
import type { Time } from "lightweight-charts";

export type ChartData = {
  time: Time;
  value: number;
};


export function extractTickValues(ticks: [string, number][]) {
  return ticks.map((x) => x[1]);
}

export async function postTickerMomentum(
  ticker: string,
  interval: string,
  ticks_values: number[]
) {
  const res = await fetch(`/ticker/momentum`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ticks: ticks_values, ticker, interval }),
  });
  return await res.json();
}

export async function postTickerMacd(
  ticker: string,
  interval: string,
  ticks_values: number[],
  short: number,
  long: number,
  signal: number
) {
  const res = await fetch(`/ticker/macd`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ticks: ticks_values,
      ticker,
      interval,
      short,
      long,
      signal,
    }),
  });
  return await res.json();
}

export async function postMacdId(short: number, long: number, signal: number) {
  const res = await fetch(`/macd/id`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      short,
      long,
      signal,
    }),
  });
  return await res.text();
}

export async function postMacdEmaId(
  short: number,
  long: number,
  signal: number
) {
  const res = await fetch(`/macd/ema-id`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      short,
      long,
      signal,
    }),
  });
  return await res.text();
}

export function mapToPrice(json: any) {
  return json.map((x: any) => ({ time: x.datetime / 1000, value: x.Close }));
}

export type Oscilator = { color: string; data: ChartData[], lineStyle?: LineStyle };
export type OscilatorHash = { [key: string]: Oscilator };

export function mapToEmas(json: any, ticks: [string, number][]) {
  let emas: OscilatorHash = {};
  for (const [color, value] of ticks) {
    emas[value] = {
      color: color,
      data: json.map((x: any) => ({
        time: x.datetime / 1000,
        value: x[`${value}_ema`],
      })),
    };
  }
  return emas;
}

export function mapToMomentumOscilator(json: any, ticks: [string, number][]) {
  let emas: OscilatorHash = {};
  for (const [color, value] of ticks) {
    emas[value] = {
      color: color,
      data: json.map((x: any) => ({
        time: x.datetime / 1000,
        value: x[`${value}_momentum`],
      })),
    };
  }
  emas["one"] = {
    color: "gray",
    data: json.map((x: any) => ({
      time: x.datetime / 1000,
      value: 1,
    })),
  };
  return emas;
}

export function mapToMacdOscilator(
  json: any,
  id: string,
  ema_id: string
) {
  let macdHash: OscilatorHash = {};
  macdHash["macd"] = {
    color: "blue",
    data: json.map((x: any) => ({time: x.datetime / 1000, value: x[id]})),
    lineStyle: LineStyle.Solid,
  }
  macdHash["signal_macd"] = {
    color: "red",
    data: json.map((x: any) => ({time: x.datetime / 1000, value: x[ema_id]})),
    lineStyle: LineStyle.Dashed,
  }
  macdHash["zero"]={
    color: "gray",
    data: json.map((x: any) => ({time: x.datetime / 1000, value: 0})),
    lineStyle: LineStyle.Dashed,
  }

  return macdHash
}
