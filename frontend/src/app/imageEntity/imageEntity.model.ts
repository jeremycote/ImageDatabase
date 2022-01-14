export class ImageEntity {
    constructor(
        public id: number,
        public filename: string,
        public updatedAt: Date,
        public createdAt: Date,
        public exif?: { [key: string]: string }
    ) {}
}