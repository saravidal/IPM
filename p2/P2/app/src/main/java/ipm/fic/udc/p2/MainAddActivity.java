package ipm.fic.udc.p2;


import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import java.util.ArrayList;


public class MainAddActivity extends AppCompatActivity implements OnClickListener{


    /**
     * Atributos
     */

    private EditText txAdd;
    private Button bAdd;
    private Button bCancel;

    private Category category = new Category();

    private Bundle extras;
    private ArrayList<String> names;


    /**
     * Metodos
     */

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.add_main);

        extras = getIntent().getExtras();
        names = extras.getStringArrayList("nameslist");

        txAdd = (EditText) findViewById(R.id.txAdd);
        bAdd = (Button) findViewById(R.id.btAdd);
        bCancel = (Button) findViewById(R.id.btCancel);

        category.setName("");

        bAdd.setOnClickListener(this);
        bCancel.setOnClickListener(this);
    }


    @Override
    public void onClick(View v)
    {
        switch (v.getId()) {

            case R.id.btAdd:
                category.setName(txAdd.getText().toString());
                if (search(names,category.getName()) == false) {
                    txAdd.setText("");
                    this.returnHome();
                    break;
                }
                else {
                    Toast.makeText(getApplicationContext(),
                            R.string.already_exists_toast, Toast.LENGTH_LONG).show();
                    category.setName("");
                    break;
                }

            case R.id.btCancel:
                txAdd.setText("");
                this.returnHome();
                break;
        }
    }


    public void returnHome() {
        Intent intent = new Intent();
        intent.putExtra("categoryD", category);
        setResult(RESULT_OK,intent);
        super.finish();
    }


    private boolean search (ArrayList<String> array, String name) {
        int i;
        boolean result = false;

        for (i = 0; i < array.size(); i++) {
            if (array.get(i).compareTo(name) == 0) {
                result = true;
                break;
            }
        }

        return result;
    }


}

