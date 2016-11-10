package ipm.fic.udc.p2;

import java.util.ArrayList;

import android.os.Parcel;
import android.os.Parcelable;

public class Category implements Parcelable {


    /**
     * Atributos
     */
    private String name; //nombre de la categoria
    private ArrayList<String> sublist; //lista de elementos de la categoria



    /**
     * Constructor por defecto
     */
    public Category() {
        name = "";
        sublist = new ArrayList<String>();
    }



    /**
     * Constructor para crear el objeto a partir de un parcelable
     * @param in
     */
    public Category (Parcel in) {
        name = "";
        sublist = new ArrayList<String>();
        readFromParcel(in);
    }


    /**
     * Getters y setters
     */

    public void setName(String name){
        this.name = name;
    }

    public String getName(){
        return this.name;
    }

    public void setSublist(ArrayList<String> sublist){
        this.sublist = sublist;
    }

    public ArrayList<String> getSublist(){
        return this.sublist;
    }


    /**
     * Obligatorio
     */
    @Override
    public int describeContents() {
        return 0;
    }



    /**
     * Escribir a un parcel, OJO el orden es importante, es como escribir en un archivo binario
     * @param dest Parcel donde se va a escribir
     * @param flags ver documentacion de Parcelable.writeToParcel
     */
    @Override
    public void writeToParcel(Parcel dest, int flags) {
        dest.writeString(name);
        dest.writeStringList(sublist);
    }



    /**
     * Clase para recuperar los datos de un parcel, IMPORTANTE leerlos en el mismo orden que se escribieron!
     * @param in Parcel con los datos a leer
     */
    private void readFromParcel(Parcel in) {
        name = in.readString();
        in.readStringList(sublist);
    }



    /**
     * Necesario para usarlo en arrays
     */
    public static final Parcelable.Creator<Category> CREATOR = new Parcelable.Creator<Category>() {
        public Category createFromParcel(Parcel in) {
            return new Category(in);
        }

        public Category[] newArray(int size) {
            return new Category[size];
        }
    };

}
