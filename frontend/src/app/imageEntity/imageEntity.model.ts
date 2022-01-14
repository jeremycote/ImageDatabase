export class ImageEntity {
    constructor(
        public filename: string,
        public path: string,
        public description: string,
        public id?: number,
        public updatedAt?: Date,
        public createdAt?: Date,
        public make?: String,
        public model?: String,
        public date?: String,
        public width?: number,
        public height?: number
    ) {}
}