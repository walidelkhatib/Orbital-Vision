const AWS = require('aws-sdk');
AWS.config.update({ region: 'us-east-2' });

const ddb = new AWS.DynamoDB.DocumentClient();

const dict = {
    '27424': 'aquaOrbit',
    '43013': 'noaaOrbit',
    '37849': 'snppOrbit'
}

exports.handler = async (event, context) => {
    const params = {
        TableName: 'orbits-czml-V2',
        Limit: 1,
        ScanIndexForward: false,
        KeyConditionExpression: "ItemName = :name",
        ExpressionAttributeValues: {
            ':name': dict[event.queryStringParameters.noradId]
        }
    }
    try {
        const data = await ddb.query(params).promise();
        return {statusCode: 200, body: JSON.stringify(data.Items[0].orbitsJson)}
    } catch (e) {
        return {statusCode: 500, body: e}
    }
};
