import React, { useState } from 'react';
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const InvestorDashboard = () => {
  const [matches, setMatches] = useState([
    {
      id: 1,
      type: "Technical Patents Group",
      investors: ["Marc Andreessen", "Sam Altman", "Jeff Bezos"],
      rawScore: 0.8,
      calibratedScore: 0.65,
      signals: {
        idea: {
          "Technical IP": 0.9,
          "Novel Approach": 0.85
        },
        execution: {
          "Team Background": 0.7,
          "Market Validation": 0.4
        }
      },
      history: {
        similarCases: 120,
        actualSuccess: 78
      }
    },
    {
      id: 2,
      type: "Monopoly Patents Group",
      investors: ["Peter Thiel", "Josh Wolfe", "Mike Maples Jr"],
      rawScore: 0.75,
      calibratedScore: 0.60,
      signals: {
        idea: {
          "Monopoly Potential": 0.95,
          "Market Defensibility": 0.80
        },
        execution: {
          "Scientific Depth": 0.85,
          "IP Strategy": 0.75
        }
      },
      history: {
        similarCases: 90,
        actualSuccess: 54
      }
    }
  ]);

  const InvestorMatrix = () => (
    <div className="grid grid-cols-2 gap-4 mb-6">
      <Card className="p-4 bg-blue-50">
        <h3 className="font-bold mb-2">Patents as Execution</h3>
        <div className="space-y-2">
          <p className="text-sm font-medium">Andreessen, Altman, Bezos</p>
          <ul className="text-sm list-disc pl-4">
            <li>Technical depth focus</li>
            <li>Product shipping history</li>
            <li>Team execution ability</li>
          </ul>
        </div>
      </Card>

      <Card className="p-4 bg-green-50">
        <h3 className="font-bold mb-2">Patents as Moat</h3>
        <div className="space-y-2">
          <p className="text-sm font-medium">Thiel, Wolfe, Maples</p>
          <ul className="text-sm list-disc pl-4">
            <li>Monopoly potential</li>
            <li>Market defensibility</li>
            <li>Scientific breakthrough</li>
          </ul>
        </div>
      </Card>

      <Card className="p-4 bg-purple-50">
        <h3 className="font-bold mb-2">Team Over Patents</h3>
        <div className="space-y-2">
          <p className="text-sm font-medium">Graham, Ravikant, Dixon</p>
          <ul className="text-sm list-disc pl-4">
            <li>Rapid execution</li>
            <li>Market understanding</li>
            <li>Customer traction</li>
          </ul>
        </div>
      </Card>

      <Card className="p-4 bg-yellow-50">
        <h3 className="font-bold mb-2">Innovation Patents</h3>
        <div className="space-y-2">
          <p className="text-sm font-medium">Srinivasan, Boyle</p>
          <ul className="text-sm list-disc pl-4">
            <li>Technical novelty</li>
            <li>Regulatory fit</li>
            <li>Market timing</li>
          </ul>
        </div>
      </Card>
    </div>
  );

  const CalibrationPlot = ({ match }) => {
    const calibrationData = [
      { bin: "0-20%", predicted: 0.1, actual: 0.08 },
      { bin: "20-40%", predicted: 0.3, actual: 0.25 },
      { bin: "40-60%", predicted: 0.5, actual: 0.45 },
      { bin: "60-80%", predicted: 0.7, actual: 0.62 },
      { bin: "80-100%", predicted: 0.9, actual: 0.71 }
    ];

    return (
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={calibrationData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="bin" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Line type="monotone" dataKey="predicted" stroke="#8884d8" name="Predicted" />
            <Line type="monotone" dataKey="actual" stroke="#82ca9d" name="Actual" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const MatchCard = ({ match }) => (
    <Card className="mb-4">
      <CardContent className="p-4">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h3 className="text-lg font-medium">{match.type}</h3>
            <div className="text-sm text-gray-500">{match.investors.join(", ")}</div>
          </div>
          <div className="text-sm">
            <div className="text-gray-500">Raw Score: {(match.rawScore * 100).toFixed()}%</div>
            <div className="font-medium">Calibrated: {(match.calibratedScore * 100).toFixed()}%</div>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <h4 className="font-medium mb-2">Idea Signals</h4>
            {Object.entries(match.signals.idea).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span>{key}</span>
                <span>{(value * 100).toFixed()}%</span>
              </div>
            ))}
          </div>
          <div>
            <h4 className="font-medium mb-2">Execution Signals</h4>
            {Object.entries(match.signals.execution).map(([key, value]) => (
              <div key={key} className="flex justify-between">
                <span>{key}</span>
                <span>{(value * 100).toFixed()}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="mt-4">
          <h4 className="font-medium mb-2">Historical Calibration</h4>
          <div className="text-sm text-gray-600">
            Based on {match.history.similarCases} similar cases,
            {match.history.actualSuccess} succeeded
            ({((match.history.actualSuccess / match.history.similarCases) * 100).toFixed()}% actual success rate)
          </div>
          <CalibrationPlot match={match} />
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="max-w-4xl mx-auto p-4">
      <Tabs defaultValue="matrix">
        <TabsList>
          <TabsTrigger value="matrix">Investor Matrix</TabsTrigger>
          <TabsTrigger value="matches">Match Analysis</TabsTrigger>
          <TabsTrigger value="calibration">Calibration Details</TabsTrigger>
        </TabsList>

        <TabsContent value="matrix">
          <InvestorMatrix />
        </TabsContent>

        <TabsContent value="matches">
          {matches.map(match => (
            <MatchCard key={match.id} match={match} />
          ))}
        </TabsContent>

        <TabsContent value="calibration">
          <Card>
            <CardContent className="p-4">
              <h3 className="text-lg font-medium mb-4">Overall Calibration Analysis</h3>
              <CalibrationPlot match={matches[0]} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default InvestorDashboard;