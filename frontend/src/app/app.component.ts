import { Component } from '@angular/core';
import { Subscription } from 'rxjs';
import { ImageEntity } from './imageEntity/imageEntity.model';
import { ImageEntityApiService } from './imageEntity/imageEntity-api.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'frontend';
  imagesListSubs: Subscription;
  imagesList: ImageEntity[] = [];

  constructor(private imagesApi: ImageEntityApiService){
    this.imagesListSubs = this.imagesApi
    .getExams()
    .subscribe(res => {
        this.imagesList = res;
      },
      console.error
    );
  }

  ngOnInit() {
    /*
    this.imagesListSubs = this.imagesApi
      .getExams()
      .subscribe(res => {
          this.imagesList = res;
        },
        console.error
      );
      */
  }

  ngOnDestroy() {
    this.imagesListSubs.unsubscribe();
  }
}
