from flask import Flask,request,jsonify,render_template
import pickle
app = Flask(__name__)
pickle_in = open("gradient_boosting.pkl", 'rb')
model = pickle.load(pickle_in)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')



@app.route("/predict", methods=['POST'])
def car_prediction():
    if request.method =='POST':

        Present_Price=request.form['Present_Price']
        Kms_Driven=request.form['Kms_Driven']
        Owner = request.form['Owner']
        Total_Year=request.form['Total_Year']
        Seller_Type_Manual = 0
        Fuel_Type_Diesel=0
        Fuel_Type_CNG = 0
        Fuel_Type=request.form['Fuel_Type']
        if Fuel_Type=='Petrol':
            Fuel_Type_Petrol=1
            Fuel_Type_CNG=0
            Fuel_Type_Diesel=0
        elif Fuel_Type=='Diesel':
            Fuel_Type_Petrol=0
            Fuel_Type_CNG=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_CNG=1
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=0


        Seller_Type=request.form['Seller_Type']
        if Seller_Type=='Dealer':
            Seller_Type_Dealer=1
            Seller_Type_Manual=0
        else:
            Seller_Type_Dealer=0
            Seller_Type_Manual=1

        Transmission_Automatic=0
        Transmission=request.form['Transmission']
        if Transmission=='Manual':
            Transmission_Manual=1
            Transmission_Automatic=0
        else:
            Transmission_Manual=0
            Transmission_Automatic=1

        prediction=model.predict([[Present_Price,Kms_Driven,Owner,Total_Year,Fuel_Type_CNG,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Dealer,Seller_Type_Manual,Transmission_Automatic,Transmission_Manual]])
        output=round(prediction[0],2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at {}".format(output))
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run()